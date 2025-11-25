"""
FastAPI orchestrator server: REST API for discovering tools, running pipelines, and querying audit logs.
Endpoints:
  GET  /tools              - list all available tools
  POST /run               - execute a single tool or pipeline
  GET  /runs              - list recent tool executions
  GET  /run/{run_id}      - get metadata for specific run
  GET  /pipelines         - list recent pipelines
  GET  /pipeline/{pipeline_id} - get full pipeline log
  GET  /stats             - journal statistics
"""

import json
from typing import List, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src.orchestrator.executor import load_registry, execute_tool
from src.orchestrator.pipeline import run_pipeline
from src.orchestrator.monitoring import (
    list_runs, read_run_meta, list_pipelines, read_pipeline,
    get_run_by_id, get_tool_runs, get_journal_stats
)

app = FastAPI(
    title="Orchestrator API",
    description="Systems integration orchestrator for chaining legacy tools and generating audit trails.",
    version="1.0.0"
)

# Mount static files (dashboard)
STATIC_DIR = Path(__file__).parents[2] / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", include_in_schema=False)
def root():
    """Redirect to dashboard."""
    return FileResponse(str(STATIC_DIR / "index.html"))

# Request models
class ToolRequest(BaseModel):
    tool_id: str
    input_text: str = ""
    timeout: int = 120

class PipelineRequest(BaseModel):
    tools: List[str]
    initial_input: str = ""
    pipeline_name: str = ""

# Routes
@app.get("/tools", tags=["Discovery"])
def list_tools():
    """List all available tools from registry."""
    registry = load_registry()
    tools = []
    for tool_id, tool in registry.items():
        tools.append({
            "id": tool_id,
            "name": tool.get("name"),
            "description": tool.get("description"),
            "category": tool.get("category"),
            "trusted": tool.get("trusted", False)
        })
    return {"tools": tools, "total": len(tools)}

@app.post("/run/tool", tags=["Execution"])
def run_tool(req: ToolRequest):
    """Execute a single tool and return metadata."""
    try:
        meta = execute_tool(req.tool_id, input_text=req.input_text, timeout=req.timeout)
        return {
            "status": "success",
            "run_id": meta["run_id"],
            "tool_id": meta["tool_id"],
            "exit_code": meta["exit_code"],
            "output_file": meta["output_file"],
            "stderr_file": meta["stderr_file"]
        }
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/run/pipeline", tags=["Execution"])
def run_pipeline_endpoint(req: PipelineRequest):
    """Execute a pipeline (sequence of chained tools)."""
    try:
        # Validate all tools exist
        registry = load_registry()
        for tool_id in req.tools:
            if tool_id not in registry:
                raise ValueError(f"Tool not found: {tool_id}")
        
        # Run pipeline
        result = run_pipeline(req.tools, initial_input=req.initial_input, pipeline_name=req.pipeline_name)
        return {
            "status": "success",
            "pipeline_id": result["pipeline_id"],
            "pipeline_name": result["pipeline_name"],
            "tools": result["tools"],
            "num_steps": result["num_steps"],
            "steps_summary": [
                {"tool_id": s["tool_id"], "exit_code": s["exit_code"]}
                for s in result["steps"]
            ]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/runs", tags=["Audit"])
def get_runs(limit: int = 50):
    """List recent tool executions."""
    runs = list_runs(limit=limit)
    meta_list = []
    for run_file in runs[:limit]:
        meta = read_run_meta(run_file)
        if meta:
            meta_list.append({
                "run_id": meta.get("run_id"),
                "tool_id": meta.get("tool_id"),
                "tool_name": meta.get("tool_name"),
                "exit_code": meta.get("exit_code"),
                "start": meta.get("start"),
                "end": meta.get("end")
            })
    return {"runs": meta_list, "total": len(meta_list)}

@app.get("/run/{run_id}", tags=["Audit"])
def get_run(run_id: str):
    """Get metadata for a specific tool execution."""
    meta = get_run_by_id(run_id)
    if not meta:
        raise HTTPException(status_code=404, detail=f"Run not found: {run_id}")
    return meta

@app.get("/pipelines", tags=["Audit"])
def get_pipelines(limit: int = 50):
    """List recent pipelines."""
    pipelines = list_pipelines(limit=limit)
    pipeline_list = []
    for pipeline_file in pipelines[:limit]:
        p = read_pipeline(pipeline_file)
        if p:
            pipeline_list.append({
                "pipeline_id": p.get("pipeline_id"),
                "pipeline_name": p.get("pipeline_name"),
                "tools": p.get("tools"),
                "num_steps": p.get("num_steps")
            })
    return {"pipelines": pipeline_list, "total": len(pipeline_list)}

@app.get("/pipeline/{pipeline_id}", tags=["Audit"])
def get_pipeline_detail(pipeline_id: str):
    """Get full details of a pipeline execution."""
    # Try to find pipeline by ID
    for pipeline_file in list_pipelines(limit=100):
        p = read_pipeline(pipeline_file)
        if p and p.get("pipeline_id") == pipeline_id:
            return p
    raise HTTPException(status_code=404, detail=f"Pipeline not found: {pipeline_id}")

@app.get("/stats", tags=["Audit"])
def get_stats():
    """Get journal statistics."""
    return get_journal_stats()

@app.get("/health", tags=["Health"])
def health():
    """Health check."""
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
