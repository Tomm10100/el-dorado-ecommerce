"""
Research Client Script
Uses Brave Search MCP to gather business intelligence
"""

import sys
import os
import json
from datetime import datetime

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from modules.mcp_integrations.execution.brave_search_connector import BraveSearchMCP

def research_prospect(company_name: str, save_to_file: bool = True):
    """
    Conduct deep research on a prospect
    """
    print(f"[START] research on: {company_name}")
    mcp = BraveSearchMCP()
    
    # 1. Company Overview (Deep Scrape)
    print("...scraping homepage content")
    try:
        # Try to guess URL if not provided
        if "." in company_name:
            url = f"https://{company_name}"
        else:
            # Fallback to search to find URL, then scrape
            search_result = mcp.search(f"{company_name} official website", num_results=1)
            url = search_result[0]['url'] if search_result else None
            
        print(f"...reading {url}")
        
        # Simple scraping (using widespread libraries or built-in tools logic simulation)
        # Using requests directly here as we are in a script
        import requests
        from bs4 import BeautifulSoup
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        resp = requests.get(url, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Get text from paragraphs and headers
            text_content = ' '.join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2', 'h3'])])
            overview = f"WEBSITE CONTENT ({url}):\n{text_content[:4000]}..." # Truncate to avoid token limits
        else:
            overview = f"Could not scrape {url} (Status {resp.status_code}). Fallback to search overview."
            overview += str(mcp.research_company(company_name))
            
    except Exception as e:
        print(f"[WARN] Scraping failed: {e}")
        overview = mcp.research_company(company_name)
    
    # 2. Tech Stack Analysis (The "X-Ray")
    print("...analyzing tech stack signals")
    # We ask specifically for CMS, frameworks, and tools
    tech_stack = mcp.search(f"site:{company_name}.com built with technology stack", num_results=3)
    
    # 3. Hiring Signals (The "Need")
    print("...checking hiring needs")
    # Hiring for 'manual' roles indicates automation potential
    hiring = mcp.search(f"{company_name} hiring 'data entry' 'customer support' 'social media manager'", num_results=3)
    
    # 4. Recent News / Pain Points
    print("...finding strategic context")
    news = mcp.search(f"{company_name} challenges problems growth strategy 2024", num_results=4)
    
    # Compile Report
    report = {
        "company": company_name,
        "timestamp": datetime.now().isoformat(),
        "overview": overview,
        "tech_signals": [r['title'] + ": " + r['description'] for r in tech_stack],
        "hiring_signals": [r['title'] for r in hiring],
        "market_signals": [r['title'] + ": " + r['description'] for r in news]
    }
    
    if save_to_file:
        # Save to module's .tmp/research
        output_dir = os.path.join(os.path.dirname(__file__), "../.tmp/research")
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{company_name.lower().replace(' ', '_')}_research.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"[SUCCESS] Research saved to: {filepath}")
        
    return report

if __name__ == "__main__":
    if len(sys.argv) > 1:
        company = sys.argv[1]
        research_prospect(company)
    else:
        print("Usage: py research_client.py 'Company Name'")
