import sys
import os
import json

# Fix imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from modules.mcp_integrations.execution.brave_search_connector import BraveSearchMCP

def search_safe():
    try:
        mcp = BraveSearchMCP()
        results = mcp.search("replit external api access token 2024", num_results=3)
        
        # Safe printing for Windows console
        for r in results:
            title = r['title'].encode('ascii', 'ignore').decode()
            url = r['url'].encode('ascii', 'ignore').decode()
            print(f"Title: {title}")
            print(f"URL: {url}")
            print("-" * 20)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    search_safe()
