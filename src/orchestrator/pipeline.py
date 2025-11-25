"""
Pipeline: chains tools together (output of one → input of next).
Records pipeline runs in Legacy_Journal for audit trail.
"""

import json
from pathlib import Path
from typing import List, Dict, Any

from .executor import execute_tool, JOURNAL, TMP

def run_pipeline(pipeline: List[str], initial_input: str = "", pipeline_name: str = "") -> Dict[str, Any]:
    """
    Run a sequence of tools where output of tool N becomes input of tool N+1.
    
    Args:
        pipeline: list of tool_ids in order
        initial_input: input text for the first tool
        pipeline_name: optional human-readable name
    
    Returns:
        dict with pipeline_id, steps (metadata from each tool), final output
    """
    if not pipeline:
        raise ValueError("Pipeline must contain at least one tool")

    context_input = initial_input
    steps = []

    for tool_id in pipeline:
        # Execute tool with current context as input
        meta = execute_tool(tool_id, input_text=context_input)
        steps.append(meta)

        # Load output to feed into next tool
        out_path = Path(meta["output_file"])
        if out_path.exists():
            context_input = out_path.read_text(encoding="utf-8")
        else:
            context_input = ""

    # Aggregate results
    pipeline_id = steps[0]["run_id"] if steps else "empty_pipeline"
    
    pipeline_log = {
        "pipeline_id": pipeline_id,
        "pipeline_name": pipeline_name or f"pipeline_{pipeline_id}",
        "tools": pipeline,
        "num_steps": len(steps),
        "steps": steps,
        "final_output": context_input[:1000]  # store first 1000 chars for reference
    }

    # Write full pipeline log to journal
    log_path = JOURNAL / f"pipeline_{pipeline_id}.json"
    log_path.write_text(json.dumps(pipeline_log, indent=2), encoding="utf-8")

    return pipeline_log
