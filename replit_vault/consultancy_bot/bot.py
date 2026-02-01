"""
ConsultancyBot - Unified Interface
Orchestrates the complete consultancy workflow from research to proposal generation

This is the main entry point for the consultancy automation system.
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, Optional

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from replit_vault.consultancy_bot.competitor_research import CompetitorResearcher
from replit_vault.consultancy_bot.proposal_generator import ProposalGenerator

# Import with proper module path (underscore, not hyphen)
import importlib
research_funding_module = importlib.import_module('modules.client-automation.execution.research_funding')
FundingResearcher = research_funding_module.FundingResearcher

generate_strategy_module = importlib.import_module('modules.client-automation.execution.generate_strategy')
generate_strategy = generate_strategy_module.generate_strategy

try:
    research_client_module = importlib.import_module('modules.client-automation.execution.research_client')
    research_client = research_client_module.research_client
except (ImportError, AttributeError):
    research_client = None


class ConsultancyBot:
    """
    Unified consultancy automation bot
    
    Orchestrates the complete workflow:
    1. Client research (company website, tech stack, team)
    2. Competitor research (industry-specific)
    3. Funding research (grants, tax credits)
    4. Strategy generation (AI-powered opportunities)
    5. Proposal generation (template-based)
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize the ConsultancyBot
        
        Args:
            verbose: Print progress messages
        """
        self.verbose = verbose
        self.competitor_researcher = CompetitorResearcher()
        self.funding_researcher = FundingResearcher()
        self.proposal_generator = ProposalGenerator()
        
        # Storage paths
        self.storage_dir = os.path.join(os.path.dirname(__file__), "../storage/consultancy")
        os.makedirs(self.storage_dir, exist_ok=True)
    
    def _log(self, message: str):
        """Print log message if verbose"""
        if self.verbose:
            print(message)
    
    def run(
        self,
        company_url: str,
        industry: str,
        company_name: Optional[str] = None,
        location: str = "Canada",
        num_competitors: int = 5
    ) -> Dict:
        """
        Run the complete consultancy workflow
        
        Args:
            company_url: URL of the client's website
            industry: Industry sector (e.g., "jewelry e-commerce", "SaaS CRM")
            company_name: Optional company name (extracted if not provided)
            location: Geographic market
            num_competitors: Number of competitors to analyze
            
        Returns:
            Dict with all research data and file paths
        """
        self._log("\n" + "="*70)
        self._log("🤖 ConsultancyBot - Complete Consultancy Automation")
        self._log("="*70)
        self._log(f"\n📍 Target: {company_url}")
        self._log(f"🏭 Industry: {industry}")
        self._log(f"🌍 Location: {location}")
        
        results = {
            "company_url": company_url,
            "industry": industry,
            "location": location,
            "timestamp": datetime.now().isoformat(),
            "steps_completed": [],
            "data": {},
            "files": {},
            "errors": []
        }
        
        # Step 1: Client Research
        self._log("\n" + "="*70)
        self._log("📊 STEP 1: Client Research")
        self._log("="*70)
        try:
            client_data = self._research_client(company_url, company_name)
            results["data"]["client"] = client_data
            results["steps_completed"].append("client_research")
            
            # Extract company name if not provided
            if not company_name:
                company_name = client_data.get("company_name", "Client")
            results["company_name"] = company_name
            
            self._log(f"✅ Client research completed for: {company_name}")
        except Exception as e:
            error_msg = f"Client research failed: {e}"
            self._log(f"❌ {error_msg}")
            results["errors"].append(error_msg)
            # Continue anyway with provided company name
            if not company_name:
                company_name = "Client"
            results["company_name"] = company_name
        
        # Step 2: Competitor Research
        self._log("\n" + "="*70)
        self._log("🏆 STEP 2: Competitor Research")
        self._log("="*70)
        try:
            competitor_data = self.competitor_researcher.research_competitors(
                industry, 
                location, 
                num_competitors
            )
            results["data"]["competitors"] = competitor_data
            
            # Save competitor research
            comp_file = self.competitor_researcher.save_research(competitor_data, company_name)
            results["files"]["competitors"] = comp_file
            results["steps_completed"].append("competitor_research")
            
            self._log(f"✅ Competitor research completed: {len(competitor_data['competitors'])} competitors analyzed")
        except Exception as e:
            error_msg = f"Competitor research failed: {e}"
            self._log(f"❌ {error_msg}")
            results["errors"].append(error_msg)
            results["data"]["competitors"] = {"competitors": [], "competitive_gaps": []}
        
        # Step 3: Funding Research
        self._log("\n" + "="*70)
        self._log("💰 STEP 3: Funding Research")
        self._log("="*70)
        try:
            funding_data = self.funding_researcher.research_funding(
                company_name,
                industry,
                location
            )
            results["data"]["funding"] = funding_data
            
            # Save funding research
            funding_file = self._save_funding_research(funding_data, company_name)
            results["files"]["funding"] = funding_file
            results["steps_completed"].append("funding_research")
            
            self._log(f"✅ Funding research completed: {len(funding_data['opportunities'])} opportunities found")
        except Exception as e:
            error_msg = f"Funding research failed: {e}"
            self._log(f"❌ {error_msg}")
            results["errors"].append(error_msg)
            results["data"]["funding"] = {}
        
        # Step 4: Strategy Generation
        self._log("\n" + "="*70)
        self._log("🎯 STEP 4: Strategy Generation")
        self._log("="*70)
        try:
            # Combine all research for strategy
            research_data = {
                "client": results["data"].get("client", {}),
                "competitors": results["data"].get("competitors", {}),
                "funding": results["data"].get("funding", {}),
                "industry": industry,
                "location": location
            }
            
            strategy_data = generate_strategy(company_name, research_data, save_to_file=False)
            results["data"]["strategy"] = strategy_data
            
            # Save strategy
            strategy_file = self._save_strategy(strategy_data, company_name)
            results["files"]["strategy"] = strategy_file
            results["steps_completed"].append("strategy_generation")
            
            opportunities_count = len(strategy_data.get("opportunities", []))
            self._log(f"✅ Strategy generated: {opportunities_count} opportunities identified")
        except Exception as e:
            error_msg = f"Strategy generation failed: {e}"
            self._log(f"❌ {error_msg}")
            results["errors"].append(error_msg)
            results["data"]["strategy"] = {}
        
        # Step 5: Proposal Generation
        self._log("\n" + "="*70)
        self._log("📄 STEP 5: Proposal Generation")
        self._log("="*70)
        try:
            proposal_content = self.proposal_generator.generate_executive_summary(
                company_name,
                industry,
                results["data"].get("strategy", {}),
                results["data"].get("competitors", {}),
                results["data"].get("funding", {})
            )
            
            # Save proposal
            proposal_file = self.proposal_generator.save_proposal(
                proposal_content,
                company_name,
                "executive_summary"
            )
            results["files"]["proposal"] = proposal_file
            results["steps_completed"].append("proposal_generation")
            
            self._log(f"✅ Executive summary proposal generated")
        except Exception as e:
            error_msg = f"Proposal generation failed: {e}"
            self._log(f"❌ {error_msg}")
            results["errors"].append(error_msg)
        
        # Final Summary
        self._log("\n" + "="*70)
        self._log("🎉 CONSULTANCY WORKFLOW COMPLETE")
        self._log("="*70)
        self._log(f"\n✅ Steps completed: {len(results['steps_completed'])}/5")
        for step in results['steps_completed']:
            self._log(f"   ✓ {step}")
        
        if results['errors']:
            self._log(f"\n⚠️  Errors encountered: {len(results['errors'])}")
            for error in results['errors']:
                self._log(f"   • {error}")
        
        self._log("\n📁 Generated files:")
        for file_type, filepath in results['files'].items():
            self._log(f"   • {file_type}: {filepath}")
        
        self._log("\n" + "="*70)
        
        return results
    
    def _research_client(self, company_url: str, company_name: Optional[str] = None) -> Dict:
        """
        Research the client company
        Uses existing research_client.py if available
        """
        try:
            # Try to use the existing research_client function
            return research_client(company_url, save_to_file=False)
        except Exception as e:
            self._log(f"[WARN] Full client research failed, using basic data: {e}")
            # Return basic data
            return {
                "company_name": company_name or "Client Company",
                "url": company_url,
                "timestamp": datetime.now().isoformat()
            }
    
    def _save_funding_research(self, funding_data: Dict, company_name: str) -> str:
        """Save funding research to file"""
        output_dir = os.path.join(self.storage_dir, "funding")
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{company_name.lower().replace(' ', '_')}_funding_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(funding_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def _save_strategy(self, strategy_data: Dict, company_name: str) -> str:
        """Save strategy to file"""
        output_dir = os.path.join(self.storage_dir, "strategy")
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{company_name.lower().replace(' ', '_')}_strategy_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(strategy_data, f, indent=2, ensure_ascii=False)
        
        return filepath


def run_consultancy(
    company_url: str,
    industry: str,
    company_name: Optional[str] = None,
    location: str = "Canada",
    num_competitors: int = 5
) -> Dict:
    """
    Convenience function to run the complete consultancy workflow
    
    Args:
        company_url: URL of the client's website
        industry: Industry sector
        company_name: Optional company name
        location: Geographic market
        num_competitors: Number of competitors to analyze
        
    Returns:
        Dict with all research data and file paths
    """
    bot = ConsultancyBot(verbose=True)
    return bot.run(company_url, industry, company_name, location, num_competitors)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        url = sys.argv[1]
        industry = sys.argv[2]
        company = sys.argv[3] if len(sys.argv) > 3 else None
        location = sys.argv[4] if len(sys.argv) > 4 else "Canada"
        
        results = run_consultancy(url, industry, company, location)
        
        print("\n" + "="*70)
        print("📊 RESULTS SUMMARY")
        print("="*70)
        print(f"\nCompany: {results['company_name']}")
        print(f"Industry: {results['industry']}")
        print(f"Steps completed: {len(results['steps_completed'])}/5")
        
        if results.get('files', {}).get('proposal'):
            print(f"\n📄 Proposal: {results['files']['proposal']}")
        
    else:
        print("Usage: python bot.py <company_url> <industry> [company_name] [location]")
        print("\nExample:")
        print("  python bot.py https://example.com 'SaaS CRM' 'TechCorp' 'USA'")
        print("  python bot.py https://jewelry-store.com 'jewelry e-commerce' 'JewelCo'")
