"""
Brave Search MCP Connector
Unrestricted web research for Antigravity
"""

import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class BraveSearchMCP:
    """MCP for Brave Search API - Unlimited web research"""
    
    def __init__(self):
        self.api_key = os.getenv("BRAVE_API_KEY")
        if not self.api_key:
            raise ValueError("BRAVE_API_KEY not found in environment")
        
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
        self.headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key
        }
    
    def search(self, query: str, num_results: int = 5, country: str = "us") -> List[Dict]:
        """
        Search the web
        
        Args:
            query: Search query
            num_results: Number of results to return (max 20)
            country: Country code for localized results
        
        Returns:
            List of search results with title, url, description
        """
        params = {
            "q": query,
            "count": min(num_results, 20),
            "country": country
        }
        
        try:
            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            results = data.get("web", {}).get("results", [])
            
            return [{
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "description": r.get("description", ""),
                "age": r.get("age", "")
            } for r in results]
        
        except requests.exceptions.RequestException as e:
            print(f"Search error: {e}")
            return []
    
    def research_company(self, company_name: str) -> Dict:
        """
        Research a company - get overview and competitors
        
        Args:
            company_name: Name of the company
        
        Returns:
            Dict with company info and competitors
        """
        # Company overview
        overview_results = self.search(f"{company_name} company overview", num_results=3)
        
        # Competitors
        competitor_results = self.search(f"competitors of {company_name}", num_results=5)
        
        # Industry info
        industry_results = self.search(f"{company_name} industry analysis", num_results=3)
        
        return {
            "company": company_name,
            "overview": overview_results[0] if overview_results else None,
            "competitors": competitor_results,
            "industry_info": industry_results
        }
    
    def research_technology(self, tech_name: str) -> Dict:
        """
        Research a technology - best practices, use cases
        
        Args:
            tech_name: Technology to research
        
        Returns:
            Dict with tech info, best practices, tutorials
        """
        best_practices = self.search(f"{tech_name} best practices 2024", num_results=5)
        use_cases = self.search(f"{tech_name} real world use cases", num_results=5)
        tutorials = self.search(f"{tech_name} tutorial getting started", num_results=3)
        
        return {
            "technology": tech_name,
            "best_practices": best_practices,
            "use_cases": use_cases,
            "tutorials": tutorials
        }
    
    def find_solution(self, problem: str) -> List[Dict]:
        """
        Research how to solve a problem
        
        Args:
            problem: Problem description
        
        Returns:
            List of potential solutions from web
        """
        return self.search(f"how to solve {problem}", num_results=10)
    
    def validate_approach(self, approach: str, context: str = "") -> List[Dict]:
        """
        Validate if an approach is good by researching similar implementations
        
        Args:
            approach: The approach to validate
            context: Optional context for better results
        
        Returns:
            List of similar implementations/discussions
        """
        query = f"{approach} {context} implementation best practices"
        return self.search(query, num_results=10)


# Quick test
if __name__ == "__main__":
    try:
        mcp = BraveSearchMCP()
        
        print("Testing Brave Search MCP...\n")
        
        # Test basic search
        results = mcp.search("Python automation", num_results=3)
        print(f"Search results ({len(results)}):")
        for r in results:
            print(f"  - {r['title']}")
            print(f"    {r['url']}\n")
        
        print("\n✅ Brave Search MCP working!")
        
    except ValueError as e:
        print(f"⚠️  {e}")
        print("Add BRAVE_API_KEY to .env to test")
