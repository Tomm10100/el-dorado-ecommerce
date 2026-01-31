"""
Funding Intelligence Module
Research available grants, tax incentives, and funding programs for prospects
"""

import sys
import os
import json
from datetime import datetime

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from modules.mcp_integrations.execution.brave_search_connector import BraveSearchMCP


class FundingResearcher:
    """Research funding opportunities for clients"""
    
    def __init__(self):
        self.mcp = BraveSearchMCP()
        
        # Funding databases to check
        self.funding_sources = {
            "canada_federal": [
                "IRAP (Industrial Research Assistance Program)",
                "SR&ED Tax Credit",
                "CanExport Innovation",
                "Canada Digital Adoption Program (CDAP)"
            ],
            "canada_provincial": [
                "Ontario Digital Main Street",
                "Quebec C2AI Program", 
                "BC Tech Fund",
                "Alberta Innovates"
            ],
            "usa_federal": [
                "SBIR/STTR Grants",
                "Economic Development Administration (EDA)",
                "Manufacturing Extension Partnership (MEP)"
            ],
            "industry_specific": [
                "Clean Tech Fund",
                "AgTech Innovation Fund",
                "Healthcare IT Modernization Grants"
            ]
        }
    
    def research_funding(self, company_name: str, industry: str = None, location: str = None):
        """
        Find funding opportunities for a specific company
        
        Args:
            company_name: Name of the company
            industry: Industry sector (optional, helps narrow results)
            location: Geographic location (country/province/state)
        """
        print(f"[FUNDING] Researching opportunities for: {company_name}")
        
        results = {
            "company": company_name,
            "industry": industry,
            "location": location,
            "timestamp": datetime.now().isoformat(),
            "opportunities": [],
            "tax_incentives": [],
            "quick_wins": []
        }
        
        # 1. Search for active grants
        print("...searching federal grants")
        grant_queries = [
            f"Canada federal grants {industry or 'technology'} automation AI 2024 2025",
            f"IRAP funding eligibility {industry or 'small business'} automation",
            f"SR&ED tax credit {industry or 'software development'} eligibility",
            f"CDAP digital adoption program boost grant automation"
        ]
        
        if location and "USA" in location.upper():
            grant_queries.extend([
                f"USA federal grants {industry or 'technology'} automation AI 2024",
                f"SBIR STTR grants {industry or 'small business'} automation eligibility"
            ])
        
        for query in grant_queries:
            try:
                search_results = self.mcp.search(query, num_results=3)
                for result in search_results:
                    results["opportunities"].append({
                        "title": result.get('title'),
                        "description": result.get('description'),
                        "url": result.get('url'),
                        "source": query.split()[0]
                    })
            except Exception as e:
                print(f"[WARN] Grant search failed for '{query}': {e}")
        
        # 2. Tax Incentives Research
        print("...researching tax incentives")
        tax_queries = [
            f"SR&ED tax credit software development {location or 'Canada'} 2024",
            f"R&D tax incentives {industry or 'technology'} {location or 'North America'}",
            f"automation investment tax credits {location or 'Canada'} eligibility"
        ]
        
        for query in tax_queries:
            try:
                search_results = self.mcp.search(query, num_results=2)
                for result in search_results:
                    results["tax_incentives"].append({
                        "title": result.get('title'),
                        "description": result.get('description'),
                        "url": result.get('url')
                    })
            except Exception as e:
                print(f"[WARN] Tax search failed: {e}")
        
        # 3. Quick Win Programs (immediate eligibility)
        print("...finding quick-win programs")
        quick_win_queries = [
            "CDAP Boost Your Business Technology grant application 2025",
            "Digital Main Street Ontario small business grant",
            "Google for Startups Canada funding",
            f"{industry or 'small business'} innovation voucher program {location or 'Canada'}"
        ]
        
        for query in quick_win_queries:
            try:
                search_results = self.mcp.search(query, num_results=2)
                for result in search_results:
                    results["quick_wins"].append({
                        "title": result.get('title'),
                        "description": result.get('description'),
                        "url": result.get('url'),
                        "type": "Quick Win"
                    })
            except Exception as e:
                print(f"[WARN] Quick win search failed: {e}")
        
        return results
    
    def analyze_eligibility(self, company_data: dict, funding_data: dict):
        """
        Analyze which funding programs the company is likely eligible for
        Uses AI to match company profile to funding criteria
        """
        print("[FUNDING] Analyzing eligibility...")
        
        from core.lib.api_client import APIClient
        
        prompt = f"""
You are a funding specialist. Analyze this company and determine which funding programs they are likely eligible for.

COMPANY DATA:
{json.dumps(company_data, indent=2)}

AVAILABLE FUNDING:
{json.dumps(funding_data, indent=2)}

OUTPUT FORMAT (JSON):
{{
    "high_probability": [
        {{
            "program": "Program name",
            "eligibility_score": "90%",
            "reasoning": "Why they qualify",
            "estimated_amount": "$15,000-$100,000",
            "application_complexity": "Low/Medium/High",
            "next_steps": "Specific action items"
        }}
    ],
    "medium_probability": [...],
    "requires_more_info": [...]
}}

Be specific. Reference actual criteria from the funding descriptions.
"""
        
        try:
            client = APIClient()
            response = client.call_gemini(prompt)
            
            # Parse JSON response
            clean_json = response.replace("```json", "").replace("```", "").strip()
            analysis = json.loads(clean_json)
            
            return analysis
        
        except Exception as e:
            print(f"[ERROR] Eligibility analysis failed: {e}")
            return {"error": str(e)}


def research_funding_opportunities(company_name: str, industry: str = None, location: str = "Canada", save_to_file: bool = True):
    """
    Main function to research funding opportunities
    """
    researcher = FundingResearcher()
    
    # Get funding data
    funding_data = researcher.research_funding(company_name, industry, location)
    
    # Save results
    if save_to_file:
        output_dir = os.path.join(os.path.dirname(__file__), "../.tmp/funding")
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{company_name.lower().replace(' ', '_')}_funding.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(funding_data, f, indent=2)
        
        print(f"[SUCCESS] Funding research saved to: {filepath}")
    
    return funding_data


if __name__ == "__main__":
    if len(sys.argv) > 1:
        company = sys.argv[1]
        industry = sys.argv[2] if len(sys.argv) > 2 else None
        location = sys.argv[3] if len(sys.argv) > 3 else "Canada"
        
        funding_data = research_funding_opportunities(company, industry, location)
        
        print("\n" + "="*60)
        print(f"Found {len(funding_data.get('opportunities', []))} grant opportunities")
        print(f"Found {len(funding_data.get('tax_incentives', []))} tax incentives")
        print(f"Found {len(funding_data.get('quick_wins', []))} quick-win programs")
        print("="*60)
        
    else:
        print("Usage: python research_funding.py 'Company Name' [Industry] [Location]")
        print("Example: python research_funding.py 'TechCorp' 'SaaS' 'Canada'")
