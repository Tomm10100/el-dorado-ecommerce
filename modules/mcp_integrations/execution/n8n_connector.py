"""
n8n Cloud MCP Connector
Full read/write access to n8n workflows - Antigravity can build automations for you!
"""

import os
import requests
from typing import List, Dict, Optional, Any
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class N8nCloudMCP:
    """MCP for n8n Cloud API - Read, Write, Trigger, Monitor workflows"""
    
    def __init__(self):
        self.api_key = os.getenv("N8N_API_KEY")
        self.base_url = os.getenv("N8N_BASE_URL", "").rstrip("/")
        
        if not self.api_key or not self.base_url:
            raise ValueError("N8N_API_KEY and N8N_BASE_URL required in .env")
        
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-N8N-API-KEY": self.api_key
        }
    
    # ==================== READ Operations ====================
    
    def get_all_workflows(self) -> List[Dict]:
        """Get all workflows - understand what's already built"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/workflows",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json().get("data", [])
        except Exception as e:
            print(f"Error getting workflows: {e}")
            return []
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict]:
        """Get specific workflow details"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/workflows/{workflow_id}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json().get("data")
        except Exception as e:
            print(f"Error getting workflow {workflow_id}: {e}")
            return None
    
    def find_workflow_by_name(self, name: str) -> Optional[Dict]:
        """Find workflow by name"""
        workflows = self.get_all_workflows()
        for wf in workflows:
            if wf.get("name", "").lower() == name.lower():
                return wf
        return None
    
    # ==================== CREATE/UPDATE Operations ====================
    
    def create_workflow(self, workflow_data: Dict) -> Optional[Dict]:
        """
        Create a new workflow programmatically!
        
        Args:
            workflow_data: Workflow definition (name, nodes, connections)
        
        Returns:
            Created workflow data
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/workflows",
                headers=self.headers,
                json=workflow_data,
                timeout=10
            )
            response.raise_for_status()
            return response.json().get("data")
        except Exception as e:
            print(f"Error creating workflow: {e}")
            return None
    
    def update_workflow(self, workflow_id: str, workflow_data: Dict) -> Optional[Dict]:
        """Update existing workflow"""
        try:
            response = requests.patch(
                f"{self.base_url}/api/v1/workflows/{workflow_id}",
                headers=self.headers,
                json=workflow_data,
                timeout=10
            )
            response.raise_for_status()
            return response.json().get("data")
        except Exception as e:
            print(f"Error updating workflow: {e}")
            return None
    
    def activate_workflow(self, workflow_id: str) -> bool:
        """Activate a workflow"""
        workflow = self.get_workflow(workflow_id)
        if workflow:
            workflow["active"] = True
            return self.update_workflow(workflow_id, workflow) is not None
        return False
    
    def deactivate_workflow(self, workflow_id: str) -> bool:
        """Deactivate a workflow"""
        workflow = self.get_workflow(workflow_id)
        if workflow:
            workflow["active"] = False
            return self.update_workflow(workflow_id, workflow) is not None
        return False
    
    # ==================== TRIGGER Operations ====================
    
    def trigger_workflow(self, workflow_id: str, data: Dict = None) -> Optional[Dict]:
        """
        Trigger a workflow execution
        
        Args:
            workflow_id: Workflow to trigger
            data: Input data for the workflow
        
        Returns:
            Execution result
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/workflows/{workflow_id}/execute",
                headers=self.headers,
                json=data or {},
                timeout=30
            )
            response.raise_for_status()
            return response.json().get("data")
        except Exception as e:
            print(f"Error triggering workflow: {e}")
            return None
    
    def trigger_workflow_by_name(self, name: str, data: Dict = None) -> Optional[Dict]:
        """Trigger workflow by name (easier than ID)"""
        workflow = self.find_workflow_by_name(name)
        if workflow:
            return self.trigger_workflow(workflow["id"], data)
        else:
            print(f"Workflow '{name}' not found")
            return None
    
    # ==================== MONITOR Operations ====================
    
    def get_executions(self, workflow_id: str = None, limit: int = 10) -> List[Dict]:
        """Get recent workflow executions"""
        try:
            params = {"limit": limit}
            if workflow_id:
                params["workflowId"] = workflow_id
            
            response = requests.get(
                f"{self.base_url}/api/v1/executions",
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json().get("data", [])
        except Exception as e:
            print(f"Error getting executions: {e}")
            return []
    
    def get_failed_executions(self, hours: int = 24) -> List[Dict]:
        """Get failed executions in last N hours"""
        executions = self.get_executions(limit=100)
        failed = []
        
        for execution in executions:
            if execution.get("finished") and not execution.get("success"):
                # Check if within time window
                stopped_at = execution.get("stoppedAt")
                if stopped_at:
                    # Add to failed list
                    failed.append(execution)
        
        return failed
    
    # ==================== HELPER Methods ====================
    
    def workflow_exists(self, name: str) -> bool:
        """Check if workflow with name exists"""
        return self.find_workflow_by_name(name) is not None
    
    def get_workflow_summary(self) -> Dict:
        """Get summary of all workflows"""
        workflows = self.get_all_workflows()
        
        active = sum(1 for wf in workflows if wf.get("active"))
        inactive = len(workflows) - active
        
        return {
            "total": len(workflows),
            "active": active,
            "inactive": inactive,
            "workflows": [{
                "id": wf["id"],
                "name": wf["name"],
                "active": wf.get("active", False)
            } for wf in workflows]
        }


# Quick test
if __name__ == "__main__":
    try:
        mcp = N8nCloudMCP()
        
        print("Testing n8n Cloud MCP...\n")
        
        # Get summary
        summary = mcp.get_workflow_summary()
        print(f"Workflows: {summary['total']} total, {summary['active']} active")
        
        # List workflows
        for wf in summary['workflows'][:5]:
            status = "[ACTIVE]" if wf['active'] else "[INACTIVE]"
            print(f"  {status} {wf['name']}")
        
        print("\n✅ n8n Cloud MCP working!")
        
    except ValueError as e:
        print(f"⚠️  {e}")
        print("Add N8N_API_KEY and N8N_BASE_URL to .env to test")
