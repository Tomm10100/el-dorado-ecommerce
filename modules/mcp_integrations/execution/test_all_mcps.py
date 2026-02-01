"""
Test Suite for All MCP Connectors
Verifies that Antigravity's "nervous system" is functioning
"""

import os
import sys
from dotenv import load_dotenv

# Add project root to sys.path
import os
import sys

# Ensure we can import from project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Standard imports
from modules.mcp_integrations.execution.replit_db_connector import ReplitDBMCP
from modules.mcp_integrations.execution.replit_fs_connector import ReplitFSMCP
from modules.mcp_integrations.execution.brave_search_connector import BraveSearchMCP
from modules.mcp_integrations.execution.n8n_connector import N8nCloudMCP

load_dotenv()

def print_header(title):
    print(f"\n{'='*60}")
    print(f" TESTING: {title}")
    print(f"{'='*60}")

def test_replit_db():
    print_header("Replit DB (Memory)")
    try:
        mcp = ReplitDBMCP()
        print(f"Storage Type: {mcp.storage_type}")
        
        # Write
        mcp.set("antigravity_test_key", "hello_world")
        # Read
        val = mcp.get("antigravity_test_key")
        print(f"Read/Write Test: {' Passed' if val == 'hello_world' else ' Failed'}")
        
        # Log test
        mcp.log_automation_run("test_suite", "success", {"message": "All systems go"})
        logs = mcp.get_automation_logs("test_suite", 1)
        print(f"Logging Test: {' Passed' if logs else ' Failed'}")
        
    except Exception as e:
        print(f" Error: {e}")

def test_replit_fs():
    print_header("Replit FS (Vision)")
    try:
        mcp = ReplitFSMCP()
        if not mcp.token:
            print(" Skipped (No REPLIT_TOKEN)")
        else:
            repls = mcp.list_repls()
            print(f"Connection: {' Connected' if repls is not None else ' Failed'}")
            print(f"Repls Found: {len(repls)}")
            
    except Exception as e:
        print(f" Error: {e}")

def test_brave_search():
    print_header("Brave Search (Research)")
    try:
        mcp = BraveSearchMCP()
        results = mcp.search("InnovLead AI consulting", num_results=1)
        if results:
            print(f"Search:  Connected")
            print(f"Result: {results[0]['title']}")
        else:
            print("Search:  No results or failed")
            
    except Exception as e:
        print(f" Error: {e}")

def test_n8n():
    print_header("n8n Cloud (Action)")
    try:
        mcp = N8nCloudMCP()
        summary = mcp.get_workflow_summary()
        print(f"Connection:  Connected")
        print(f"Workflows: {summary['total']} total")
        
    except ValueError:
        print(" Skipped (Missing Credentials)")
    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    print("\n ANTIGRAVITY MCP SYSTEM DIAGNOSTIC")
    test_replit_db()
    test_replit_fs()
    test_brave_search()
    test_n8n()
    print("\n Diagnostics Complete.")

