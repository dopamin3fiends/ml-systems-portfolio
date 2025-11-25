"""
Executor: runs individual orchestrator tools, captures output, logs to Legacy_Journal.
"""

import json
import uuid
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

ROOT = Path(__file__).parents[2]
JOURNAL = ROOT / "Legacy_Journal"
PRIVATE = ROOT / "Private_Legacy"
TMP = ROOT / "data" / "tmp"

# Create directories if needed
for d in (JOURNAL, PRIVATE, TMP):
    d.mkdir(parents=True, exist_ok=True)

REGISTRY_PATH = Path(__file__).parent / "registry.json"

def load_registry() -> Dict[str, Any]:
    """Load tool registry."""
    with open(REGISTRY_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh).get("tools", {})

def _write_file(path: Path, data: str) -> None:
    """Safely write file with parent directory creation."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8")

def execute_tool(tool_id: str, input_text: str = "", timeout: int = 120) -> Dict[str, Any]:
    """
    Execute a tool from the registry.
    - tool_id: identifier in registry.json
    - input_text: stdin/file content for the tool
    - timeout: max seconds to run
    Returns metadata dict with run_id, exit code, output paths, timestamps.
    """
    registry = load_registry()
    if tool_id not in registry:
        raise KeyError(f"Tool not found in registry: {tool_id}")

    tool = registry[tool_id]
    run_id = uuid.uuid4().hex
    start = datetime.utcnow().isoformat() + "Z"

    # Prepare input/output files in tmp
    input_file = TMP / f"{run_id}_{tool_id}.in.txt"
    output_file = TMP / f"{run_id}_{tool_id}.out.txt"
    stderr_file = TMP / f"{run_id}_{tool_id}.err.txt"
    
    _write_file(input_file, input_text or "")

    # Build command: substitute {input} and {output} in args_template
    args_template = tool.get("args_template", [])
    args = []
    for arg in args_template:
        arg = arg.replace("{input}", str(input_file))
        arg = arg.replace("{output}", str(output_file))
        args.append(arg)

    cmd = list(tool.get("command", [])) + args

    # Log plan before execution
    plan = {
        "run_id": run_id,
        "tool_id": tool_id,
        "tool_name": tool.get("name"),
        "cmd": cmd,
        "start": start,
        "cwd": str(PRIVATE)
    }
    _write_file(JOURNAL / f"{run_id}_{tool_id}_plan.json", json.dumps(plan, indent=2))

    # Execute
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(PRIVATE)
        )
        exit_code = proc.returncode
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
    except subprocess.TimeoutExpired as e:
        exit_code = 124
        stdout = ""
        stderr = f"Timeout after {timeout}s: {str(e)}"
    except Exception as e:
        exit_code = -1
        stdout = ""
        stderr = f"Execution error: {str(e)}"

    end = datetime.utcnow().isoformat() + "Z"

    # Write outputs to files
    _write_file(output_file, stdout)
    _write_file(stderr_file, stderr)

    # Record execution metadata
    meta = {
        "run_id": run_id,
        "tool_id": tool_id,
        "tool_name": tool.get("name"),
        "category": tool.get("category"),
        "cmd": cmd,
        "start": start,
        "end": end,
        "exit_code": exit_code,
        "output_file": str(output_file),
        "stderr_file": str(stderr_file),
        "input_size": len(input_text),
        "output_size": len(stdout),
        "error_size": len(stderr)
    }

    # Write metadata to journal
    _write_file(JOURNAL / f"{run_id}_{tool_id}_meta.json", json.dumps(meta, indent=2))

    return meta
