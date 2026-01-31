"""
Test Script for ConsultancyBot
Simple validation of the package structure and functionality
"""

import sys
import os
import json
from datetime import datetime

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def test_imports():
    """Test that all modules can be imported"""
    print("="*70)
    print("TEST 1: Package Imports")
    print("="*70)
    
    try:
        from replit_vault.consultancy_bot import ConsultancyBot
        print("[OK] ConsultancyBot imported successfully")
    except Exception as e:
        print(f"[FAIL] ConsultancyBot import failed: {e}")
        return False
    
    try:
        from replit_vault.consultancy_bot import CompetitorResearcher
        print("[OK] CompetitorResearcher imported successfully")
    except Exception as e:
        print(f"[FAIL] CompetitorResearcher import failed: {e}")
        return False
    
    try:
        from replit_vault.consultancy_bot import ProposalGenerator
        print("[OK] ProposalGenerator imported successfully")
    except Exception as e:
        print(f"[FAIL] ProposalGenerator import failed: {e}")
        return False
    
    return True


def test_proposal_generator():
    """Test proposal generator with mock data"""
    print("\n" + "="*70)
    print("TEST 2: Proposal Generator")
    print("="*70)
    
    try:
        from replit_vault.consultancy_bot import ProposalGenerator
        
        generator = ProposalGenerator()
        print("[OK] ProposalGenerator initialized")
        
        # Mock data
        mock_strategy = {
            "executive_summary": "Test company has great potential for automation.",
            "opportunities": [
                {
                    "title": "Process Automation",
                    "pain_point": "Manual data entry",
                    "proposed_solution": "Implement n8n workflows",
                    "roi_impact": "Save 20 hours/week",
                    "confidence": "High"
                },
                {
                    "title": "Marketing Automation",
                    "pain_point": "No email sequences",
                    "proposed_solution": "Deploy email automation",
                    "roi_impact": "30% conversion increase",
                    "confidence": "Medium"
                }
            ]
        }
        
        mock_competitors = {
            "industry": "SaaS",
            "location": "Canada",
            "competitors": [
                {
                    "name": "Competitor A",
                    "positioning": "Market leader",
                    "threat_level": "HIGH",
                    "weaknesses": ["Expensive", "Poor support"]
                },
                {
                    "name": "Competitor B",
                    "positioning": "Budget option",
                    "threat_level": "MEDIUM",
                    "weaknesses": ["Limited features"]
                }
            ],
            "competitive_gaps": [
                {
                    "gap_name": "Automation Integration",
                    "description": "No competitors offer deep automation",
                    "opportunity": "Build automation-first platform",
                    "difficulty": "Medium",
                    "potential_impact": "High"
                }
            ]
        }
        
        mock_funding = {
            "opportunities": [
                {
                    "title": "CDAP Grant",
                    "description": "Digital adoption program",
                    "url": "https://example.com"
                }
            ],
            "tax_incentives": [
                {
                    "title": "SR&ED Tax Credit",
                    "description": "R&D tax credit"
                }
            ]
        }
        
        # Generate proposal
        proposal = generator.generate_executive_summary(
            company_name="TestCorp",
            industry="SaaS Testing",
            strategy_data=mock_strategy,
            competitor_data=mock_competitors,
            funding_data=mock_funding
        )
        
        print(f"[OK] Proposal generated: {len(proposal)} characters")
        
        # Check key sections exist
        required_sections = [
            "TestCorp",
            "Executive Summary",
            "Market Intelligence",
            "Strategic Analysis",
            "InnovLead Solution",
            "Implementation Roadmap"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in proposal:
                missing_sections.append(section)
        
        if missing_sections:
            print(f"[WARN] Missing sections: {', '.join(missing_sections)}")
        else:
            print("[OK] All required sections present")
        
        # Test saving (to temp location)
        try:
            test_dir = os.path.join(os.path.dirname(__file__), "../storage/proposals/test_output")
            os.makedirs(test_dir, exist_ok=True)
            
            test_file = os.path.join(test_dir, "test_proposal.md")
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(proposal)
            
            print(f"[OK] Proposal saved to: {test_file}")
            
            # Cleanup
            os.remove(test_file)
            print("[OK] Test file cleaned up")
            
        except Exception as e:
            print(f"[WARN] Save test failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Proposal generator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_competitor_researcher():
    """Test competitor researcher structure"""
    print("\n" + "="*70)
    print("TEST 3: Competitor Researcher")
    print("="*70)
    
    try:
        from replit_vault.consultancy_bot import CompetitorResearcher
        
        researcher = CompetitorResearcher()
        print("[OK] CompetitorResearcher initialized")
        
        # Test methods exist
        methods = [
            'research_competitors',
            '_analyze_competitor',
            '_generate_market_insights',
            '_identify_gaps',
            'save_research'
        ]
        
        for method in methods:
            if hasattr(researcher, method):
                print(f"[OK] Method '{method}' exists")
            else:
                print(f"[FAIL] Method '{method}' missing")
                return False
        
        print("[OK] CompetitorResearcher structure validated")
        return True
        
    except Exception as e:
        print(f"[FAIL] Competitor researcher test failed: {e}")
        return False


def test_consultancy_bot():
    """Test ConsultancyBot class structure"""
    print("\n" + "="*70)
    print("TEST 4: ConsultancyBot Class")
    print("="*70)
    
    try:
        from replit_vault.consultancy_bot import ConsultancyBot
        
        bot = ConsultancyBot(verbose=False)
        print("[OK] ConsultancyBot initialized")
        
        # Test attributes
        attributes = [
            'competitor_researcher',
            'funding_researcher',
            'proposal_generator',
            'storage_dir'
        ]
        
        for attr in attributes:
            if hasattr(bot, attr):
                print(f"[OK] Attribute '{attr}' exists")
            else:
                print(f"[FAIL] Attribute '{attr}' missing")
                return False
        
        # Test methods exist
        methods = [
            'run',
            '_log',
            '_research_client',
            '_save_funding_research',
            '_save_strategy'
        ]
        
        for method in methods:
            if hasattr(bot, method):
                print(f"[OK] Method '{method}' exists")
            else:
                print(f"[FAIL] Method '{method}' missing")
                return False
        
        print("[OK] ConsultancyBot structure validated")
        return True
        
    except Exception as e:
        print(f"[FAIL] ConsultancyBot test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_template_exists():
    """Test that template file exists"""
    print("\n" + "="*70)
    print("TEST 5: Template Files")
    print("="*70)
    
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    template_file = os.path.join(template_dir, "executive_summary.md")
    
    if os.path.exists(template_file):
        print(f"[OK] Template exists: {template_file}")
        
        # Check file size
        size = os.path.getsize(template_file)
        print(f"[OK] Template size: {size} bytes")
        
        # Check it contains Jinja2 syntax
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if '{{' in content and '{%' in content:
            print("[OK] Template contains Jinja2 syntax")
        else:
            print("[WARN] Template may not have Jinja2 syntax")
        
        return True
    else:
        print(f"[FAIL] Template not found: {template_file}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("ConsultancyBot Package Tests")
    print("="*70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = []
    
    # Run tests
    results.append(("Package Imports", test_imports()))
    results.append(("Proposal Generator", test_proposal_generator()))
    results.append(("Competitor Researcher", test_competitor_researcher()))
    results.append(("ConsultancyBot Class", test_consultancy_bot()))
    results.append(("Template Files", test_template_exists()))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} - {test_name}")
    
    print("\n" + "="*70)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed!")
    else:
        print(f"{total - passed} test(s) failed")
    
    print("="*70 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
