"""
Enhanced Multi-Dimensional Client Research
Combines: Company Intel + Financial Analysis + Competitor Benchmarking + Industry Trends
"""

import sys
import os
import json
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from modules.mcp_integrations.execution.brave_search_connector import BraveSearchMCP


class EnhancedResearcher:
    """Comprehensive multi-dimensional research"""
    
    def __init__(self):
        self.mcp = BraveSearchMCP()
        # Configure Gemini
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.ai_model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def call_gemini(self, prompt: str) -> str:
        """Call Gemini API"""
        try:
            response = self.ai_model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"[ERROR] Gemini API call failed: {e}")
            return "{}"
    
    def research_company_overview(self, company_name: str, url: str = None):
        """Deep dive into company overview"""
        print(f"[RESEARCH] Company Overview: {company_name}")
        
        try:
            # Try to scrape website
            if not url:
                if "." in company_name:
                    url = f"https://{company_name}"
                else:
                    search_result = self.mcp.search(f"{company_name} official website", num_results=1)
                    url = search_result[0]['url'] if search_result else None
            
            if url:
                print(f"...scraping {url}")
                import requests
                from bs4 import BeautifulSoup
                
                headers = {'User-Agent': 'Mozilla/5.0'}
                resp = requests.get(url, headers=headers, timeout=10)
                
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    text_content = ' '.join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])])
                    overview = text_content[:5000]
                else:
                    overview = str(self.mcp.research_company(company_name))
            else:
                overview = str(self.mcp.research_company(company_name))
                
        except Exception as e:
            print(f"[WARN] Scraping failed: {e}")
            overview = str(self.mcp.research_company(company_name))
        
        return {
            "url": url,
            "content": overview,
            "scraped_at": datetime.now().isoformat()
        }
    
    def research_financial_signals(self, company_name: str):
        """Analyze financial health and growth signals"""
        print(f"[RESEARCH] Financial Signals: {company_name}")
        
        queries = [
            f"{company_name} revenue growth 2024",
            f"{company_name} funding raised series investors",
            f"{company_name} employee count headcount growth",
            f"{company_name} expansion new markets locations",
            f"{company_name} acquisition merger news 2024"
        ]
        
        signals = []
        for query in queries:
            try:
                results = self.mcp.search(query, num_results=2)
                for result in results:
                    signals.append({
                        "signal_type": query.split()[1],  # revenue, funding, employee, etc.
                        "title": result.get('title'),
                        "description": result.get('description'),
                        "url": result.get('url')
                    })
            except Exception as e:
                print(f"[WARN] Financial search failed: {e}")
        
        return signals
    
    def research_competitors(self, company_name: str, industry: str = None):
        """Identify and analyze competitors"""
        print(f"[RESEARCH] Competitor Analysis: {company_name}")
        
        # Find competitors
        competitor_query = f"{company_name} competitors alternatives {industry or 'industry'} comparison"
        
        try:
            results = self.mcp.search(competitor_query, num_results=5)
            competitors_raw = [r.get('title') for r in results]
            
            # Use AI to extract actual competitor names
            extraction_prompt = f"""
From this search data about {company_name}'s competitors, extract a clean list of 3-5 actual competitor company names.

SEARCH RESULTS:
{json.dumps(competitors_raw, indent=2)}

OUTPUT FORMAT (JSON):
{{
    "competitors": ["Company A", "Company B", "Company C"]
}}

Only include real company names, not generic descriptions.
"""
            
            response = self.call_gemini(extraction_prompt)
            clean_json = response.replace("```json", "").replace("```", "").strip()
            competitor_list = json.loads(clean_json).get("competitors", [])
            
            # Research each competitor's automation maturity
            competitor_analysis = []
            for comp in competitor_list[:3]:  # Top 3 only
                comp_queries = [
                    f"{comp} AI automation technology stack",
                    f"{comp} digital transformation strategy"
                ]
                
                comp_data = {"name": comp, "automation_signals": []}
                for query in comp_queries:
                    try:
                        comp_results = self.mcp.search(query, num_results=2)
                        for result in comp_results:
                            comp_data["automation_signals"].append(result.get('title'))
                    except:
                        pass
                
                competitor_analysis.append(comp_data)
            
            return competitor_analysis
            
        except Exception as e:
            print(f"[WARN] Competitor research failed: {e}")
            return []
    
    def research_industry_trends(self, industry: str):
        """Analyze industry-wide automation trends"""
        print(f"[RESEARCH] Industry Trends: {industry}")
        
        queries = [
            f"{industry} industry automation trends 2024 2025",
            f"{industry} AI adoption rate statistics",
            f"{industry} digital transformation challenges opportunities",
            f"{industry} emerging technology investments"
        ]
        
        trends = []
        for query in queries:
            try:
                results = self.mcp.search(query, num_results=2)
                for result in results:
                    trends.append({
                        "title": result.get('title'),
                        "description": result.get('description'),
                        "url": result.get('url')
                    })
            except Exception as e:
                print(f"[WARN] Trend search failed: {e}")
        
        return trends
    
    def research_hiring_signals(self, company_name: str):
        """Detect hiring patterns that indicate automation needs"""
        print(f"[RESEARCH] Hiring Signals: {company_name}")
        
        # Target manual/repetitive roles
        hiring_queries = [
            f"{company_name} hiring 'data entry' 'manual' jobs",
            f"{company_name} hiring 'customer support' 'customer service' positions",
            f"{company_name} hiring 'social media manager' 'content coordinator'",
            f"{company_name} hiring 'administrative assistant' 'operations coordinator'"
        ]
        
        signals = []
        for query in hiring_queries:
            try:
                results = self.mcp.search(query, num_results=2)
                for result in results:
                    signals.append({
                        "title": result.get('title'),
                        "description": result.get('description'),
                        "url": result.get('url'),
                        "automation_potential": "High"  # These roles are highly automatable
                    })
            except Exception as e:
                print(f"[WARN] Hiring search failed: {e}")
        
        return signals
    
    def synthesize_insights(self, research_data: dict):
        """Use AI to synthesize all research into actionable insights"""
        print("[RESEARCH] Synthesizing insights with AI...")
        
        prompt = f"""
You are a senior business analyst. Synthesize this multi-dimensional research into key insights.

RESEARCH DATA:
{json.dumps(research_data, indent=2)}

OUTPUT FORMAT (JSON):
{{
    "executive_summary": "2-3 sentence overview of the company's situation",
    "strengths": ["What they're doing well"],
    "pain_points": ["Identified challenges and bottlenecks"],
    "automation_readiness": "Low/Medium/High - with reasoning",
    "competitive_position": "How they compare to competitors in automation",
    "strategic_priorities": ["What they likely care about most"],
    "conversation_hooks": ["Specific talking points for sales outreach"]
}}

Be specific and actionable. Reference actual data from the research.
"""
        
        try:
            response = self.call_gemini(prompt)
            clean_json = response.replace("```json", "").replace("```", "").strip()
            insights = json.loads(clean_json)
            return insights
        except Exception as e:
            print(f"[ERROR] Insight synthesis failed: {e}")
            return {"error": str(e)}


def conduct_full_research(company_name: str, industry: str = None, url: str = None, save_to_file: bool = True):
    """
    Conduct comprehensive multi-dimensional research
    """
    print(f"\n{'='*60}")
    print(f"ENHANCED RESEARCH: {company_name}")
    print(f"{'='*60}\n")
    
    researcher = EnhancedResearcher()
    
    # Gather all dimensions
    research_data = {
        "company": company_name,
        "industry": industry,
        "timestamp": datetime.now().isoformat(),
        "overview": researcher.research_company_overview(company_name, url),
        "financial_signals": researcher.research_financial_signals(company_name),
        "competitors": researcher.research_competitors(company_name, industry),
        "industry_trends": researcher.research_industry_trends(industry or "technology"),
        "hiring_signals": researcher.research_hiring_signals(company_name)
    }
    
    # Synthesize insights
    research_data["insights"] = researcher.synthesize_insights(research_data)
    
    # Save results
    if save_to_file:
        output_dir = os.path.join(os.path.dirname(__file__), "../.tmp/research")
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{company_name.lower().replace(' ', '_')}_enhanced_research.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(research_data, f, indent=2)
        
        print(f"\n[SUCCESS] Enhanced research saved to: {filepath}")
    
    return research_data


if __name__ == "__main__":
    if len(sys.argv) > 1:
        company = sys.argv[1]
        industry = sys.argv[2] if len(sys.argv) > 2 else None
        url = sys.argv[3] if len(sys.argv) > 3 else None
        
        research = conduct_full_research(company, industry, url)
        
        print("\n" + "="*60)
        print("RESEARCH COMPLETE")
        print("="*60)
        print(f"Financial signals found: {len(research.get('financial_signals', []))}")
        print(f"Competitors identified: {len(research.get('competitors', []))}")
        print(f"Hiring signals detected: {len(research.get('hiring_signals', []))}")
        print(f"Industry trends: {len(research.get('industry_trends', []))}")
        
        if research.get('insights'):
            print(f"\nAutomation Readiness: {research['insights'].get('automation_readiness', 'N/A')}")
        
    else:
        print("Usage: python research_enhanced.py 'Company Name' [Industry] [URL]")
        print("Example: python research_enhanced.py 'Shopify' 'E-commerce' 'https://shopify.com'")
