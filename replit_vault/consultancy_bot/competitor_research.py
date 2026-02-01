"""
Dynamic Competitor Research Module
Researches real competitors in any industry using Brave Search API

This replaces the hardcoded jewelry_competitors.py with a dynamic, 
industry-agnostic system that can research competitors for any business.
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, List, Optional

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from modules.mcp_integrations.execution.brave_search_connector import BraveSearchMCP


class CompetitorResearcher:
    """Research competitors dynamically for any industry"""
    
    def __init__(self):
        self.mcp = BraveSearchMCP()
        
    def research_competitors(
        self, 
        industry: str, 
        location: str = "Canada",
        num_competitors: int = 5
    ) -> Dict:
        """
        Find and analyze real competitors in any industry
        
        Args:
            industry: Industry sector (e.g., "jewelry e-commerce", "SaaS CRM", "restaurant")
            location: Geographic market (e.g., "Canada", "USA", "Toronto")
            num_competitors: Number of competitors to analyze (default: 5)
            
        Returns:
            Dict with competitor analysis data
        """
        print(f"[COMPETITOR RESEARCH] Industry: {industry}, Location: {location}")
        
        results = {
            "industry": industry,
            "location": location,
            "timestamp": datetime.now().isoformat(),
            "competitors": [],
            "market_insights": {},
            "competitive_gaps": []
        }
        
        # 1. Find top competitors
        print("...searching for top competitors")
        competitor_queries = [
            f"top {industry} companies in {location} 2024 2025",
            f"best {industry} {location} market leaders",
            f"leading {industry} businesses {location}",
            f"{industry} market share {location}"
        ]
        
        discovered_competitors = []
        
        for query in competitor_queries:
            try:
                search_results = self.mcp.search(query, num_results=5)
                for result in search_results:
                    competitor_info = {
                        "name": self._extract_company_name(result.get('title', '')),
                        "url": result.get('url', ''),
                        "description": result.get('description', ''),
                        "source_query": query
                    }
                    # Avoid duplicates
                    if competitor_info['url'] and competitor_info['url'] not in [c['url'] for c in discovered_competitors]:
                        discovered_competitors.append(competitor_info)
                        
            except Exception as e:
                print(f"[WARN] Competitor search failed for '{query}': {e}")
        
        # Limit to requested number
        discovered_competitors = discovered_competitors[:num_competitors]
        print(f"...found {len(discovered_competitors)} competitors")
        
        # 2. Analyze each competitor
        for competitor in discovered_competitors:
            print(f"...analyzing {competitor['name']}")
            analysis = self._analyze_competitor(competitor, industry, location)
            results["competitors"].append(analysis)
        
        # 3. Extract market insights
        print("...generating market insights")
        results["market_insights"] = self._generate_market_insights(industry, location)
        
        # 4. Identify competitive gaps
        print("...identifying competitive gaps")
        results["competitive_gaps"] = self._identify_gaps(results["competitors"], industry)
        
        return results
    
    def _extract_company_name(self, title: str) -> str:
        """Extract clean company name from search result title"""
        # Remove common suffixes
        title = title.split('|')[0].split('-')[0].split(':')[0]
        # Remove year references
        for year in ['2024', '2025', '2023']:
            title = title.replace(year, '')
        return title.strip()
    
    def _analyze_competitor(self, competitor: Dict, industry: str, location: str) -> Dict:
        """
        Analyze a specific competitor using additional searches
        """
        name = competitor['name']
        
        analysis = {
            "name": name,
            "url": competitor['url'],
            "description": competitor['description'],
            "strengths": [],
            "weaknesses": [],
            "pricing_intel": [],
            "positioning": "",
            "threat_level": "UNKNOWN"
        }
        
        # Search for competitor-specific intelligence
        intel_queries = [
            f"{name} pricing {industry}",
            f"{name} reviews complaints",
            f"{name} competitive advantage",
            f"{name} market position {industry}"
        ]
        
        intel_data = []
        for query in intel_queries:
            try:
                search_results = self.mcp.search(query, num_results=3)
                for result in search_results:
                    intel_data.append({
                        "title": result.get('title', ''),
                        "description": result.get('description', ''),
                        "url": result.get('url', ''),
                        "query_type": query.split()[1] if len(query.split()) > 1 else "general"
                    })
            except Exception as e:
                print(f"[WARN] Intel search failed for '{name}': {e}")
        
        # Use AI to analyze collected intelligence
        analysis = self._ai_analyze_competitor(name, intel_data, industry, analysis)
        
        return analysis
    
    def _ai_analyze_competitor(
        self, 
        company_name: str, 
        intel_data: List[Dict], 
        industry: str,
        base_analysis: Dict
    ) -> Dict:
        """
        Use AI to analyze competitor intelligence and extract insights
        """
        try:
            from core.lib.api_client import APIClient
            
            prompt = f"""
You are a competitive intelligence analyst. Analyze this competitor data and provide structured insights.

COMPETITOR: {company_name}
INDUSTRY: {industry}

INTELLIGENCE DATA:
{json.dumps(intel_data, indent=2)}

OUTPUT FORMAT (JSON):
{{
    "strengths": ["List 3-5 key competitive strengths"],
    "weaknesses": ["List 3-5 exploitable weaknesses"],
    "pricing_intel": ["Specific pricing information found"],
    "positioning": "One-sentence market positioning summary",
    "threat_level": "HIGH/MEDIUM/LOW (based on competitive strength)",
    "key_differentiators": ["What makes them unique"],
    "opportunities_to_beat_them": ["Specific ways to compete"]
}}

Be specific and actionable. If data is limited, indicate "INSUFFICIENT DATA" for that field.
"""
            
            client = APIClient()
            response = client.call_gemini(prompt)
            
            # Parse JSON response
            clean_json = response.replace("```json", "").replace("```", "").strip()
            ai_analysis = json.loads(clean_json)
            
            # Merge with base analysis
            base_analysis.update(ai_analysis)
            
        except Exception as e:
            print(f"[WARN] AI analysis failed for {company_name}: {e}")
            # Return base analysis with defaults
            base_analysis["strengths"] = ["Established brand presence"]
            base_analysis["weaknesses"] = ["INSUFFICIENT DATA"]
            base_analysis["positioning"] = "Market participant"
            base_analysis["threat_level"] = "MEDIUM"
        
        return base_analysis
    
    def _generate_market_insights(self, industry: str, location: str) -> Dict:
        """
        Generate market-level insights for the industry
        """
        print("...researching market size and trends")
        
        insights = {
            "market_size": None,
            "growth_rate": None,
            "key_trends": [],
            "consumer_behavior": []
        }
        
        # Search for market data
        market_queries = [
            f"{industry} market size {location} 2024",
            f"{industry} trends {location} 2025",
            f"{industry} consumer behavior statistics",
            f"{industry} growth rate forecast"
        ]
        
        market_data = []
        for query in market_queries:
            try:
                search_results = self.mcp.search(query, num_results=3)
                for result in search_results:
                    market_data.append({
                        "title": result.get('title', ''),
                        "description": result.get('description', ''),
                        "url": result.get('url', '')
                    })
            except Exception as e:
                print(f"[WARN] Market search failed: {e}")
        
        # Use AI to synthesize market insights
        try:
            from core.lib.api_client import APIClient
            
            prompt = f"""
Analyze this market research data and provide key insights.

INDUSTRY: {industry}
LOCATION: {location}

MARKET DATA:
{json.dumps(market_data, indent=2)}

OUTPUT FORMAT (JSON):
{{
    "market_size": "Estimated market size with source",
    "growth_rate": "Annual growth rate percentage",
    "key_trends": ["3-5 major industry trends"],
    "consumer_behavior": ["3-5 key consumer behavior insights"],
    "market_maturity": "Emerging/Growth/Mature/Declining"
}}

Be specific and cite numbers where available.
"""
            
            client = APIClient()
            response = client.call_gemini(prompt)
            
            clean_json = response.replace("```json", "").replace("```", "").strip()
            insights = json.loads(clean_json)
            
        except Exception as e:
            print(f"[WARN] Market insights AI analysis failed: {e}")
        
        return insights
    
    def _identify_gaps(self, competitors: List[Dict], industry: str) -> List[Dict]:
        """
        Identify strategic gaps in the competitive landscape
        """
        print("...using AI to identify strategic gaps")
        
        gaps = []
        
        try:
            from core.lib.api_client import APIClient
            
            prompt = f"""
You are a strategic consultant. Analyze these competitors and identify market gaps.

INDUSTRY: {industry}

COMPETITOR ANALYSIS:
{json.dumps(competitors, indent=2)}

Identify 3-5 strategic gaps or opportunities where a new entrant could differentiate.

OUTPUT FORMAT (JSON):
{{
    "gaps": [
        {{
            "gap_name": "Short name for the opportunity",
            "description": "What's missing in the market",
            "opportunity": "How to exploit this gap",
            "difficulty": "Easy/Medium/Hard to execute",
            "potential_impact": "Low/Medium/High revenue impact"
        }}
    ]
}}

Focus on gaps that are:
1. Unserved or underserved by current competitors
2. Valued by customers
3. Feasible to execute
"""
            
            client = APIClient()
            response = client.call_gemini(prompt)
            
            clean_json = response.replace("```json", "").replace("```", "").strip()
            gap_analysis = json.loads(clean_json)
            gaps = gap_analysis.get("gaps", [])
            
        except Exception as e:
            print(f"[WARN] Gap analysis failed: {e}")
            gaps = [{
                "gap_name": "Technology Integration",
                "description": "Competitors lack modern automation",
                "opportunity": "Implement AI and automation for competitive advantage",
                "difficulty": "Medium",
                "potential_impact": "High"
            }]
        
        return gaps
    
    def save_research(self, results: Dict, company_name: str) -> str:
        """
        Save competitor research to file
        """
        output_dir = os.path.join(os.path.dirname(__file__), "../storage/consultancy/competitor_research")
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{company_name.lower().replace(' ', '_')}_competitors_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"[SUCCESS] Competitor research saved to: {filepath}")
        return filepath


def research_competitors(
    industry: str, 
    location: str = "Canada", 
    num_competitors: int = 5,
    company_name: str = None,
    save_to_file: bool = True
) -> Dict:
    """
    Main function to research competitors dynamically
    
    Args:
        industry: Industry sector to research
        location: Geographic market
        num_competitors: Number of competitors to analyze
        company_name: Optional company name for file naming
        save_to_file: Whether to save results to file
    """
    researcher = CompetitorResearcher()
    
    # Get competitor data
    results = researcher.research_competitors(industry, location, num_competitors)
    
    # Save results
    if save_to_file and company_name:
        researcher.save_research(results, company_name)
    
    return results


if __name__ == "__main__":
    if len(sys.argv) > 1:
        industry = sys.argv[1]
        location = sys.argv[2] if len(sys.argv) > 2 else "Canada"
        company = sys.argv[3] if len(sys.argv) > 3 else "Client"
        
        results = research_competitors(industry, location, company_name=company)
        
        print("\n" + "="*60)
        print(f"Found {len(results['competitors'])} competitors")
        print(f"Identified {len(results['competitive_gaps'])} strategic gaps")
        print("="*60)
        
    else:
        print("Usage: python competitor_research.py 'Industry' [Location] [CompanyName]")
        print("Example: python competitor_research.py 'SaaS CRM' 'USA' 'TechCorp'")
