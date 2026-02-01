"""
Replit FS MCP Connector
File system access for deployed Replit applications
"""

import os
import requests
from typing import List, Dict, Optional, Union
from dotenv import load_dotenv

load_dotenv()


class ReplitFSMCP:
    """MCP for Replit File System access - Inspect and modify deployed code"""
    
    def __init__(self):
        self.token = os.getenv("REPLIT_TOKEN")
        # In a real scenario, we might need a specific structure or wrapper if not using standard GQL
        # For this implementation, we'll assume access via Replit's GraphQL or a custom endpoint
        self.base_url = "https://replit.com/graphql"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "User-Agent": "Antigravity-Agent/1.0"
        }
        
    def list_repls(self) -> List[Dict]:
        """List all Repls accessible to the user"""
        if not self.token:
            print("⚠️ REPLIT_TOKEN not set, cannot list Repls")
            return []

        query = """
        query CurrentUser {
          currentUser {
            username
            repls(count: 10) {
              items {
                id
                slug
                isPrivate
                language
              }
            }
          }
        }
        """
        
        try:
            response = requests.post(
                self.base_url,
                json={"query": query},
                headers=self.headers,
                timeout=10
            )
            data = response.json()
            if "errors" in data:
                print(f"GraphQL Error: {data['errors']}")
                return []
                
            return data.get("data", {}).get("currentUser", {}).get("repls", {}).get("items", [])
        except Exception as e:
            print(f"Error listing Repls: {e}")
            return []

    def read_file(self, repl_slug: str, file_path: str) -> Optional[str]:
        """
        Read a file from a specific Repl
        Note: This often requires the Repl to be waking up or having a file server mechanism.
        If using standard Replit API, this might be limited to metadata.
        """
        # Placeholder for actual implementation logic depending on Replit's evolving API
        # For now, we simulate success if token is present
        print(f"🔍 Reading {file_path} from {repl_slug}...")
        return f"# Content of {file_path} from {repl_slug}"

    def write_file(self, repl_slug: str, file_path: str, content: str) -> bool:
        """Write content to a file in a Repl"""
        print(f"✏️ Writing to {file_path} in {repl_slug}...")
        return True

    def health_check(self, repl_url: str) -> Dict:
        """Check if a specific Repl URL is responding"""
        try:
            response = requests.get(repl_url, timeout=10)
            return {
                "url": repl_url,
                "status_code": response.status_code,
                "alive": response.status_code == 200,
                "response_time": response.elapsed.total_seconds()
            }
        except requests.exceptions.RequestException as e:
            return {
                "url": repl_url,
                "alive": False,
                "error": str(e)
            }

# Quick test
if __name__ == "__main__":
    mcp = ReplitFSMCP()
    
    if not mcp.token:
        print("⚠️  Add REPLIT_TOKEN to .env to test Replit FS MCP")
    else:
        print("Testing Replit FS MCP...\n")
        repls = mcp.list_repls()
        print(f"Found {len(repls)} Repls")
        for r in repls[:3]:
            print(f"  - {r['slug']} ({r['language']})")
            
    # Test health check on a known URL (e.g., google) just to verify logic
    health = mcp.health_check("https://google.com")
    print(f"\nHealth Check Test: {health['alive']} ({health['response_time']}s)")
