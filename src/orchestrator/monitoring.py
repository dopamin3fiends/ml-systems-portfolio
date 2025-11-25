"""
Monitoring: audit and retrieval functions for runs and pipelines.
Queries Legacy_Journal for historical data.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional

ROOT = Path(__file__).parents[2]
JOURNAL = ROOT / "Legacy_Journal"

def list_runs(limit: int = 100) -> List[str]:
    """List all tool execution metadata files."""
    runs = sorted([p.name for p in JOURNAL.glob("*_meta.json")], reverse=True)
    return runs[:limit]

def read_run_meta(run_meta_filename: str) -> Optional[Dict[str, Any]]:
    """Read metadata for a specific tool execution."""
    p = JOURNAL / run_meta_filename
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))

def list_pipelines(limit: int = 100) -> List[str]:
    """List all pipeline execution logs."""
    pipelines = sorted([p.name for p in JOURNAL.glob("pipeline_*.json")], reverse=True)
    return pipelines[:limit]

def read_pipeline(pipeline_filename: str) -> Optional[Dict[str, Any]]:
    """Read a complete pipeline execution log."""
    p = JOURNAL / pipeline_filename
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))

def get_run_by_id(run_id: str) -> Optional[Dict[str, Any]]:
    """Find a run by run_id and return its metadata."""
    for meta_file in JOURNAL.glob("*_meta.json"):
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        if meta.get("run_id") == run_id:
            return meta
    return None

def get_tool_runs(tool_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Get all runs for a specific tool."""
    runs = []
    for meta_file in sorted(JOURNAL.glob("*_meta.json"), reverse=True)[:limit*2]:
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        if meta.get("tool_id") == tool_id:
            runs.append(meta)
    return runs[:limit]

def get_journal_stats() -> Dict[str, Any]:
    """Summary statistics from the journal."""
    meta_files = list(JOURNAL.glob("*_meta.json"))
    pipeline_files = list(JOURNAL.glob("pipeline_*.json"))
    
    tool_counts = {}
    for meta_file in meta_files:
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        tool_id = meta.get("tool_id")
        tool_counts[tool_id] = tool_counts.get(tool_id, 0) + 1
    
    return {
        "total_runs": len(meta_files),
        "total_pipelines": len(pipeline_files),
        "tool_counts": tool_counts,
        "journal_path": str(JOURNAL)
    }
