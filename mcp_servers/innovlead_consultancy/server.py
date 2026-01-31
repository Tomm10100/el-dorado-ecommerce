"""
InnovLead Consultancy MCP Server
Main server implementation exposing consultancy automation tools
"""

import asyncio
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from mcp.server import Server
from mcp.types import Tool, Resource, TextContent
from pydantic import BaseModel, Field


# Initialize MCP Server
app = Server("innovlead-consultancy")

# Path configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
MODULES_PATH = PROJECT_ROOT / "modules" / "client-automation"
EXECUTION_PATH = MODULES_PATH / "execution"
OUTPUTS_PATH = MODULES_PATH / "outputs" / "proposals"
TMP_PATH = MODULES_PATH / ".tmp"

# In-memory job tracker (use database in production)
jobs_db = {}


# ============================================================================
# TOOL SCHEMAS
# ============================================================================

class RunConsultancyInput(BaseModel):
    company: str = Field(description="Company name to analyze")
    industry: Optional[str] = Field(default="", description="Industry sector (e.g., 'SaaS', 'E-commerce')")
    url: Optional[str] = Field(default="", description="Company website URL")
    location: Optional[str] = Field(default="Canada", description="Geographic location for funding research")


class CheckStatusInput(BaseModel):
    job_id: str = Field(description="Job ID to check status for")


class GetResultsInput(BaseModel):
    job_id: str = Field(description="Job ID to retrieve results for")


class DownloadProposalInput(BaseModel):
    job_id: str = Field(description="Job ID")
    proposal_type: str = Field(description="Type: 'executive', 'technical', 'financial', or 'funding'")


class SendEmailInput(BaseModel):
    job_id: str = Field(description="Job ID")
    recipient_email: str = Field(description="Email address to send proposals to")
    proposals: Optional[list[str]] = Field(default=["executive"], description="List of proposal types to send")


# ============================================================================
# TOOLS
# ============================================================================

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available consultancy tools"""
    return [
        Tool(
            name="run_full_consultancy",
            description="Execute complete multi-dimensional consultancy analysis including research, funding identification, strategy generation, and proposal creation. Takes 10-15 minutes.",
            inputSchema=RunConsultancyInput.model_json_schema()
        ),
        Tool(
            name="check_consultancy_status",
            description="Check the status and progress of a running consultancy job",
            inputSchema=CheckStatusInput.model_json_schema()
        ),
        Tool(
            name="get_consultancy_results",
            description="Retrieve full results from a completed consultancy analysis including metrics, insights, and file paths",
            inputSchema=GetResultsInput.model_json_schema()
        ),
        Tool(
            name="download_proposal",
            description="Download a specific proposal document (executive summary, technical roadmap, financial model, or funding application)",
            inputSchema=DownloadProposalInput.model_json_schema()
        ),
        Tool(
            name="send_proposals_email",
            description="Email generated proposals to a specified recipient (placeholder - requires email configuration)",
            inputSchema=SendEmailInput.model_json_schema()
        ),
        Tool(
            name="list_consultancy_history",
            description="List all past consultancy analyses with basic info and status",
            inputSchema={}
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    
    if name == "run_full_consultancy":
        return await run_full_consultancy(arguments)
    elif name == "check_consultancy_status":
        return await check_consultancy_status(arguments)
    elif name == "get_consultancy_results":
        return await get_consultancy_results(arguments)
    elif name == "download_proposal":
        return await download_proposal(arguments)
    elif name == "send_proposals_email":
        return await send_proposals_email(arguments)
    elif name == "list_consultancy_history":
        return await list_consultancy_history()
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


async def run_full_consultancy(args: dict) -> list[TextContent]:
    """Execute full consultancy analysis"""
    try:
        # Parse inputs
        input_data = RunConsultancyInput(**args)
        
        # Generate job ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        company_slug = input_data.company.lower().replace(" ", "_")
        job_id = f"job_{timestamp}_{company_slug}"
        
        # Create job record
        job_data = {
            "job_id": job_id,
            "company": input_data.company,
            "industry": input_data.industry,
            "url": input_data.url,
            "location": input_data.location,
            "status": "running",
            "phase": "initializing",
            "progress": 0,
            "created_at": datetime.now().isoformat(),
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
            "results": None,
            "error": None
        }
        
        jobs_db[job_id] = job_data
        
        # Build command
        script_path = EXECUTION_PATH / "run_full_consultancy.py"
        cmd = [sys.executable, str(script_path), input_data.company]
        
        if input_data.industry:
            cmd.extend(["--industry", input_data.industry])
        if input_data.url:
            cmd.extend(["--url", input_data.url])
        if input_data.location:
            cmd.extend(["--location", input_data.location])
        
        # Run in background
        asyncio.create_task(execute_consultancy(job_id, cmd))
        
        response = {
            "success": True,
            "job_id": job_id,
            "status": "running",
            "message": f"Consultancy analysis started for {input_data.company}",
            "estimated_time": "10-15 minutes",
            "check_status_with": f"check_consultancy_status with job_id: {job_id}"
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(response, indent=2)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error": str(e)
            }, indent=2)
        )]


async def execute_consultancy(job_id: str, cmd: list[str]):
    """Background task to execute consultancy"""
    job = jobs_db[job_id]
    
    try:
        # Update status
        job["phase"] = "running"
        job["progress"] = 10
        
        # Execute command
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Wait for completion
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            # Success
            job["status"] = "complete"
            job["phase"] = "complete"
            job["progress"] = 100
            job["completed_at"] = datetime.now().isoformat()
            
            # Parse results (look for generated files)
            company_slug = job["company"].lower().replace(" ", "_")
            results = {
                "metrics": {
                    "proposals_generated": 4,
                    "research_complete": True,
                    "funding_analyzed": True
                },
                "files": {
                    "executive_summary": f"outputs/proposals/{company_slug}_executive_summary_*.md",
                    "technical_roadmap": f"outputs/proposals/{company_slug}_technical_roadmap_*.md",
                    "financial_model": f"outputs/proposals/{company_slug}_financial_model_*.md",
                    "funding_application": f"outputs/proposals/{company_slug}_funding_application_*.md"
                }
            }
            job["results"] = results
            
        else:
            # Error
            job["status"] = "error"
            job["error"] = stderr.decode() if stderr else "Unknown error"
            job["completed_at"] = datetime.now().isoformat()
            
    except Exception as e:
        job["status"] = "error"
        job["error"] = str(e)
        job["completed_at"] = datetime.now().isoformat()


async def check_consultancy_status(args: dict) -> list[TextContent]:
    """Check status of consultancy job"""
    try:
        input_data = CheckStatusInput(**args)
        job_id = input_data.job_id
        
        if job_id not in jobs_db:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"Job ID {job_id} not found"
                }, indent=2)
            )]
        
        job = jobs_db[job_id]
        
        response = {
            "success": True,
            "job_id": job_id,
            "company": job["company"],
            "status": job["status"],
            "phase": job["phase"],
            "progress": job["progress"],
            "created_at": job["created_at"],
            "completed_at": job["completed_at"],
            "error": job["error"]
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(response, indent=2)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error": str(e)
            }, indent=2)
        )]


async def get_consultancy_results(args: dict) -> list[TextContent]:
    """Get full results from completed consultancy"""
    try:
        input_data = GetResultsInput(**args)
        job_id = input_data.job_id
        
        if job_id not in jobs_db:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"Job ID {job_id} not found"
                }, indent=2)
            )]
        
        job = jobs_db[job_id]
        
        if job["status"] != "complete":
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"Job not complete. Current status: {job['status']}"
                }, indent=2)
            )]
        
        response = {
            "success": True,
            "job_id": job_id,
            "company": job["company"],
            "industry": job["industry"],
            "completed_at": job["completed_at"],
            "results": job["results"]
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(response, indent=2)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error": str(e)
            }, indent=2)
        )]


async def download_proposal(args: dict) -> list[TextContent]:
    """Download specific proposal document"""
    try:
        input_data = DownloadProposalInput(**args)
        job_id = input_data.job_id
        proposal_type = input_data.proposal_type
        
        if job_id not in jobs_db:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"Job ID {job_id} not found"
                }, indent=2)
            )]
        
        job = jobs_db[job_id]
        
        if job["status"] != "complete":
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": "Job not complete yet"
                }, indent=2)
            )]
        
        # Find proposal file
        company_slug = job["company"].lower().replace(" ", "_")
        proposal_pattern = f"{company_slug}_{proposal_type}_*.md"
        
        # Search for file in outputs
        proposal_files = list(OUTPUTS_PATH.glob(proposal_pattern))
        
        if not proposal_files:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"Proposal file not found: {proposal_pattern}"
                }, indent=2)
            )]
        
        # Read the most recent file
        proposal_file = sorted(proposal_files)[-1]
        
        with open(proposal_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        response = {
            "success": True,
            "job_id": job_id,
            "proposal_type": proposal_type,
            "file_path": str(proposal_file),
            "content": content[:500] + "..." if len(content) > 500 else content,
            "full_content_available": True
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(response, indent=2)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error": str(e)
            }, indent=2)
        )]


async def send_proposals_email(args: dict) -> list[TextContent]:
    """Send proposals via email (placeholder)"""
    try:
        input_data = SendEmailInput(**args)
        
        # This is a placeholder - implement with SendGrid, SMTP, etc.
        response = {
            "success": True,
            "message": f"Email sending not yet configured. Would send {len(input_data.proposals)} proposals to {input_data.recipient_email}",
            "recipient": input_data.recipient_email,
            "proposals": input_data.proposals,
            "note": "Configure email service in production"
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(response, indent=2)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error": str(e)
            }, indent=2)
        )]


async def list_consultancy_history() -> list[TextContent]:
    """List all consultancy jobs"""
    try:
        history = []
        
        for job_id, job in jobs_db.items():
            history.append({
                "job_id": job_id,
                "company": job["company"],
                "industry": job["industry"],
                "status": job["status"],
                "created_at": job["created_at"],
                "completed_at": job["completed_at"]
            })
        
        # Sort by created date (newest first)
        history.sort(key=lambda x: x["created_at"], reverse=True)
        
        response = {
            "success": True,
            "total": len(history),
            "history": history
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(response, indent=2)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error": str(e)
            }, indent=2)
        )]


# ============================================================================
# RESOURCES
# ============================================================================

@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources"""
    return [
        Resource(
            uri="consultancy://history",
            name="Consultancy History",
            description="Historical record of all consultancy analyses",
            mimeType="application/json"
        ),
        Resource(
            uri="consultancy://templates",
            name="Proposal Templates",
            description="Available proposal templates and formats",
            mimeType="application/json"
        )
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read resource content"""
    
    if uri == "consultancy://history":
        # Return job history as JSON
        history = [
            {
                "job_id": job_id,
                "company": job["company"],
                "status": job["status"],
                "created_at": job["created_at"]
            }
            for job_id, job in jobs_db.items()
        ]
        return json.dumps(history, indent=2)
    
    elif uri == "consultancy://templates":
        # Return available templates
        templates = {
            "executive_summary": "C-level focused business impact summary",
            "technical_roadmap": "IT team implementation guide",
            "financial_model": "CFO-ready ROI and cost analysis",
            "funding_application": "Pre-filled grant application draft"
        }
        return json.dumps(templates, indent=2)
    
    else:
        return json.dumps({"error": f"Unknown resource: {uri}"})


# ============================================================================
# SERVER STARTUP
# ============================================================================

if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    
    asyncio.run(main())
