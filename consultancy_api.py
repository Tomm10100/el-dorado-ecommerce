"""
InnovLead Consultancy API - Direct Wrapper
Simple interface for conversational consultancy automation
"""

import sys
import subprocess
from pathlib import Path

def run_consultancy(company: str, industry: str = "", url: str = "", location: str = "Canada"):
    """Run full consultancy analysis"""
    script_path = Path("modules/client-automation/execution/run_full_consultancy.py")
    
    cmd = [sys.executable, str(script_path), company]
    
    if industry:
        cmd.extend(["--industry", industry])
    if url:
        cmd.extend(["--url", url])
    if location:
        cmd.extend(["--location", location])
    
    print(f">> Starting consultancy analysis for {company}...")
    print(f"   Industry: {industry or 'Not specified'}")
    print(f"   Location: {location}")
    print(f"   Estimated time: 10-15 minutes")
    print()
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(">> Consultancy analysis complete!")
        print()
        print("Generated proposals:")
        company_slug = company.lower().replace(" ", "_")
        print(f"   - Executive Summary: outputs/proposals/{company_slug}_executive_summary_*.md")
        print(f"   - Technical Roadmap: outputs/proposals/{company_slug}_technical_roadmap_*.md")
        print(f"   - Financial Model: outputs/proposals/{company_slug}_financial_model_*.md")
        print(f"   - Funding Application: outputs/proposals/{company_slug}_funding_application_*.md")
        return True
    else:
        print(">> Error occurred:")
        print(result.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py consultancy_api.py <company> [industry] [url] [location]")
        print("Example: py consultancy_api.py 'Tesla' 'Automotive' 'https://tesla.com' 'USA'")
        sys.exit(1)
    
    company = sys.argv[1]
    industry = sys.argv[2] if len(sys.argv) > 2 else ""
    url = sys.argv[3] if len(sys.argv) > 3 else ""
    location = sys.argv[4] if len(sys.argv) > 4 else "Canada"
    
    success = run_consultancy(company, industry, url, location)
    sys.exit(0 if success else 1)
