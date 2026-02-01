"""
Enhanced Consultancy Loop - Full Multi-Dimensional Analysis
Orchestrates: Research -> Funding -> Strategy -> Proposal Suite
This is the BEAST MODE consultancy engine
"""

import sys
import os
import json
import argparse
from datetime import datetime

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from research_enhanced import conduct_full_research
from research_funding import research_funding_opportunities
from generate_strategy import generate_strategy
from generate_proposal_suite import generate_full_proposal_suite


class ConsultancyOrchestrator:
    """Master orchestrator for full consultancy process"""
    
    def __init__(self, company_name: str, industry: str = None, url: str = None, location: str = "Canada"):
        self.company = company_name
        self.industry = industry
        self.url = url
        self.location = location
        self.start_time = datetime.now()
        
        # Results storage
        self.research_data = None
        self.funding_data = None
        self.strategy_data = None
        self.proposal_suite = None
        
        self.log_file = self._setup_logging()
    
    def _setup_logging(self):
        """Setup execution logging"""
        output_dir = os.path.join(os.path.dirname(__file__), "../.tmp/logs")
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        company_slug = self.company.lower().replace(' ', '_')
        log_path = os.path.join(output_dir, f"{company_slug}_consultancy_{timestamp}.log")
        
        return log_path
    
    def log(self, message: str, level: str = "INFO"):
        """Log message to console and file"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        
        print(log_entry)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
    
    def run_phase_1_research(self):
        """Phase 1: Multi-dimensional research"""
        self.log("="*60)
        self.log(f"PHASE 1: MULTI-DIMENSIONAL RESEARCH")
        self.log(f"Company: {self.company}")
        self.log(f"Industry: {self.industry or 'Auto-detect'}")
        self.log("="*60)
        
        try:
            self.research_data = conduct_full_research(
                company_name=self.company,
                industry=self.industry,
                url=self.url,
                save_to_file=True
            )
            
            self.log(" Research completed successfully", "SUCCESS")
            
            # Log key findings
            if self.research_data.get('insights'):
                insights = self.research_data['insights']
                self.log(f"  Automation Readiness: {insights.get('automation_readiness', 'N/A')}")
                self.log(f"  Pain Points: {len(insights.get('pain_points', []))}")
                self.log(f"  Competitors: {len(self.research_data.get('competitors', []))}")
            
            return True
            
        except Exception as e:
            self.log(f" Research failed: {e}", "ERROR")
            return False
    
    def run_phase_2_funding(self):
        """Phase 2: Funding intelligence"""
        self.log("\n" + "="*60)
        self.log("PHASE 2: FUNDING INTELLIGENCE")
        self.log("="*60)
        
        try:
            self.funding_data = research_funding_opportunities(
                company_name=self.company,
                industry=self.industry,
                location=self.location,
                save_to_file=True
            )
            
            self.log(" Funding research completed", "SUCCESS")
            
            # Log findings
            grants = len(self.funding_data.get('opportunities', []))
            tax = len(self.funding_data.get('tax_incentives', []))
            quick = len(self.funding_data.get('quick_wins', []))
            
            self.log(f"  Grant opportunities: {grants}")
            self.log(f"  Tax incentives: {tax}")
            self.log(f"  Quick-win programs: {quick}")
            
            return True
            
        except Exception as e:
            self.log(f" Funding research failed: {e}", "ERROR")
            return False
    
    def run_phase_3_strategy(self):
        """Phase 3: Strategic analysis"""
        self.log("\n" + "="*60)
        self.log("PHASE 3: STRATEGIC ANALYSIS")
        self.log("="*60)
        
        if not self.research_data:
            self.log(" No research data available", "ERROR")
            return False
        
        try:
            self.strategy_data = generate_strategy(
                company_name=self.company,
                research_data=self.research_data,
                save_to_file=True
            )
            
            self.log(" Strategy generated", "SUCCESS")
            
            # Log opportunities
            if isinstance(self.strategy_data, dict):
                opps = self.strategy_data.get('opportunities', [])
                self.log(f"  Automation opportunities: {len(opps)}")
                
                for i, opp in enumerate(opps[:3], 1):
                    self.log(f"  {i}. {opp.get('title', 'N/A')}")
            
            return True
            
        except Exception as e:
            self.log(f" Strategy generation failed: {e}", "ERROR")
            return False
    
    def run_phase_4_proposals(self):
        """Phase 4: Multi-stakeholder proposal generation"""
        self.log("\n" + "="*60)
        self.log("PHASE 4: PROPOSAL SUITE GENERATION")
        self.log("="*60)
        
        try:
            self.proposal_suite = generate_full_proposal_suite(
                company_name=self.company,
                save_to_file=True
            )
            
            self.log(" Proposal suite generated", "SUCCESS")
            self.log("   Executive Summary (C-Suite)")
            self.log("   Technical Roadmap (IT/Engineering)")
            self.log("   Financial Model (CFO)")
            self.log("   Funding Application (Grant Writer)")
            
            return True
            
        except Exception as e:
            self.log(f" Proposal generation failed: {e}", "ERROR")
            return False
    
    def generate_summary_report(self):
        """Generate execution summary"""
        self.log("\n" + "="*60)
        self.log("CONSULTANCY COMPLETE")
        self.log("="*60)
        
        elapsed = datetime.now() - self.start_time
        elapsed_min = elapsed.total_seconds() / 60
        
        self.log(f"\nExecution Time: {elapsed_min:.1f} minutes")
        self.log(f"Company: {self.company}")
        self.log(f"Industry: {self.industry or 'Auto-detected'}")
        
        self.log("\n OUTPUTS GENERATED:")
        
        company_slug = self.company.lower().replace(' ', '_')
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        outputs = [
            f"Research: .tmp/research/{company_slug}_enhanced_research.json",
            f"Funding: .tmp/funding/{company_slug}_funding.json",
            f"Strategy: .tmp/strategy/{company_slug}_strategy.json",
            f"Executive Summary: outputs/proposals/{company_slug}_executive_summary_{date_str}.md",
            f"Technical Roadmap: outputs/proposals/{company_slug}_technical_roadmap_{date_str}.md",
            f"Financial Model: outputs/proposals/{company_slug}_financial_model_{date_str}.md",
            f"Funding Application: outputs/proposals/{company_slug}_funding_application_{date_str}.md"
        ]
        
        for output in outputs:
            self.log(f"   {output}")
        
        self.log(f"\n EXECUTION LOG: {self.log_file}")
        
        self.log("\n NEXT STEPS:")
        self.log("  1. Review the Executive Summary")
        self.log("  2. Customize proposals based on specific intel")
        self.log("  3. Send to prospect with funding highlights")
        self.log("  4. Book discovery call as 'strategic advisor'")
        
        self.log("\n" + "="*60)
    
    def run(self):
        """Execute full consultancy loop"""
        self.log(f"\n{'#'*60}")
        self.log(f"# INNOVLEAD CONSULTANCY ENGINE v2.0")
        self.log(f"# Multi-Dimensional Analysis System")
        self.log(f"{'#'*60}\n")
        
        # Phase 1: Research
        if not self.run_phase_1_research():
            self.log("Consultancy aborted due to research failure", "ERROR")
            return False
        
        # Phase 2: Funding
        if not self.run_phase_2_funding():
            self.log("Warning: Continuing without funding data", "WARN")
        
        # Phase 3: Strategy
        if not self.run_phase_3_strategy():
            self.log("Consultancy aborted due to strategy failure", "ERROR")
            return False
        
        # Phase 4: Proposals
        if not self.run_phase_4_proposals():
            self.log("Warning: Proposals incomplete", "WARN")
        
        # Summary
        self.generate_summary_report()
        
        return True


def main():
    """CLI interface"""
    parser = argparse.ArgumentParser(
        description='InnovLead Enhanced Consultancy Engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_full_consultancy.py "Shopify"
  python run_full_consultancy.py "Shopify" --industry "E-commerce" --url "https://shopify.com"
  python run_full_consultancy.py "TechCorp" --industry "SaaS" --location "Canada"

This will generate:
   Multi-dimensional research report
   Funding opportunities analysis  
   Strategic automation recommendations
   4 stakeholder-specific proposal documents
        """
    )
    
    parser.add_argument('company', help='Company name')
    parser.add_argument('--industry', help='Industry sector (optional)', default=None)
    parser.add_argument('--url', help='Company website URL (optional)', default=None)
    parser.add_argument('--location', help='Geographic location (default: Canada)', default='Canada')
    
    args = parser.parse_args()
    
    # Run consultancy
    orchestrator = ConsultancyOrchestrator(
        company_name=args.company,
        industry=args.industry,
        url=args.url,
        location=args.location
    )
    
    success = orchestrator.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments - show help
        print("\n" + "="*60)
        print("InnovLead Enhanced Consultancy Engine v2.0")
        print("="*60)
        print("\nUsage:")
        print("  python run_full_consultancy.py 'Company Name' [options]")
        print("\nExamples:")
        print("  python run_full_consultancy.py 'Shopify'")
        print("  python run_full_consultancy.py 'TechCorp' --industry 'SaaS'")
        print("  python run_full_consultancy.py 'CanCorp' --location 'Canada'")
        print("\nFor detailed help:")
        print("  python run_full_consultancy.py --help")
        print()
    else:
        main()


