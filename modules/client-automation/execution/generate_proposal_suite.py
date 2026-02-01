"""
Advanced Proposal Suite Generator
Generates multi-format deliverables for different stakeholders:
- Executive Summary (C-Suite)
- Technical Roadmap (IT/Engineering)
- Financial Model (CFO)
- Funding Application Draft (Grant Writers)
"""

import sys
import os
import json
from datetime import datetime, timedelta

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from core.lib.api_client import APIClient


class ProposalSuiteGenerator:
    """Generate comprehensive proposal suite"""
    
    def __init__(self):
        self.ai = APIClient()
    
    def generate_executive_summary(self, company: str, research: dict, strategy: dict, funding: dict):
        """Generate C-Suite focused executive summary"""
        print("[PROPOSAL] Generating Executive Summary...")
        
        prompt = f"""
You are a management consultant preparing an executive briefing for the C-Suite of {company}.

RESEARCH DATA:
{json.dumps(research, indent=2)[:3000]}

STRATEGIC OPPORTUNITIES:
{json.dumps(strategy, indent=2)[:2000]}

FUNDING OPPORTUNITIES:
{json.dumps(funding, indent=2)[:2000]}

Create a concise executive summary (1-2 pages) in MARKDOWN format:

# Executive Briefing: {company} Digital Transformation

## Situation Analysis
[2-3 sentences on current state]

## Strategic Imperatives
[3 bullet points of must-dos]

## Proposed Solution
[High-level automation strategy]

## Financial Impact
- **Cost Savings**: [Estimated annual savings]
- **Revenue Opportunity**: [Growth potential]
- **Investment Required**: [Implementation cost]
- **Available Funding**: [Grants/incentives to offset]
- **Net ROI**: [Payback period]

## Competitive Advantage
[How this positions them vs competitors]

## Recommended Next Steps
1. [Immediate action]
2. [30-day milestone]
3. [90-day goal]

## Risk Mitigation
[Key risks and how we'll address them]

Be specific, use numbers, and focus on business outcomes not technology features.
"""
        
        try:
            response = self.ai.call_gemini(prompt)
            return response
        except Exception as e:
            return f"Error generating executive summary: {e}"
    
    def generate_technical_roadmap(self, company: str, research: dict, strategy: dict):
        """Generate IT/Engineering team focused technical roadmap"""
        print("[PROPOSAL] Generating Technical Roadmap...")
        
        prompt = f"""
You are a solutions architect preparing a technical implementation plan for {company}.

RESEARCH DATA:
{json.dumps(research, indent=2)[:3000]}

AUTOMATION OPPORTUNITIES:
{json.dumps(strategy, indent=2)[:2000]}

Create a detailed technical roadmap in MARKDOWN format:

# Technical Implementation Roadmap: {company}

## Current State Architecture
[Diagram-ready description of their current tech stack]

## Proposed Architecture
[Target state with automation layers]

## Implementation Phases

### Phase 1: Foundation (Weeks 1-4)
**Objectives**: [What we build]
**Technologies**: [Tools/platforms used]
**Deliverables**:
- [Specific output 1]
- [Specific output 2]
**Success Metrics**: [How we measure]

### Phase 2: Core Automation (Weeks 5-8)
[Same structure]

### Phase 3: Advanced Features (Weeks 9-12)
[Same structure]

## Technology Stack
| Layer | Technology | Purpose | Why This Choice |
|-------|-----------|---------|-----------------|
| Orchestration | n8n | Workflow automation | Open-source, flexible |
| AI Engine | Gemini 2.0 | Intelligence layer | Cost-effective, powerful |
| Data Storage | [Recommend based on needs] | | |
| Deployment | Replit/Cloud | Hosting | | 

## Integration Points
[How this connects to existing systems]

## Security & Compliance
[Data handling, access controls, compliance measures]

## Maintenance & Support
[Post-launch support model]

## Technical Risks & Mitigation
[Specific technical challenges and solutions]

Be technically accurate but accessible. Include specific tool names and configurations.
"""
        
        try:
            response = self.ai.call_gemini(prompt)
            return response
        except Exception as e:
            return f"Error generating technical roadmap: {e}"
    
    def generate_financial_model(self, company: str, strategy: dict, funding: dict):
        """Generate CFO-focused financial analysis"""
        print("[PROPOSAL] Generating Financial Model...")
        
        prompt = f"""
You are a financial analyst preparing a cost-benefit analysis for {company}'s CFO.

AUTOMATION OPPORTUNITIES:
{json.dumps(strategy, indent=2)[:2000]}

FUNDING OPPORTUNITIES:
{json.dumps(funding, indent=2)[:1500]}

Create a financial model in MARKDOWN format:

# Financial Analysis: {company} Automation Investment

## Investment Summary
| Category | Amount | Timeframe |
|----------|--------|-----------|
| **Total Investment** | $XX,XXX | 12 weeks |
| **Available Grants** | $(XX,XXX) | Upon approval |
| **Net Investment** | $XX,XXX | |
| **Annual Savings** | $XXX,XXX | Year 1+ |
| **Payback Period** | X months | |
| **3-Year ROI** | XXX% | |

## Cost Breakdown

### Implementation Costs (One-Time)
- Discovery & Planning: $X,XXX
- Development & Integration: $XX,XXX
- Testing & Training: $X,XXX
- **Total Implementation**: $XX,XXX

### Annual Operating Costs
- Platform licenses: $X,XXX/year
- API costs: $X,XXX/year
- Maintenance & support: $X,XXX/year
- **Total Annual**: $XX,XXX/year

## Savings Analysis

### Labor Cost Reduction
| Process | Current Cost | Post-Automation | Annual Savings |
|---------|-------------|-----------------|----------------|
| [Process 1] | $XX,XXX | $X,XXX | $XX,XXX |
| [Process 2] | $XX,XXX | $X,XXX | $XX,XXX |
| **Total** | | | **$XXX,XXX** |

### Revenue Opportunity
[How automation enables growth]
- Estimated new revenue: $XX,XXX/year

### Efficiency Gains
- Time saved: XXX hours/week
- Reallocation value: $XX,XXX/year

## Funding Stack
1. **[Grant Program Name]**: $XX,XXX (High probability)
   - Application deadline: [Date]
   - Requirements: [Brief]
   
2. **[Tax Credit]**: $X,XXX (Guaranteed)
   - Claim period: [Timeframe]

## Cash Flow Projection

### Year 1
- Q1: Investment phase (-$XX,XXX)
- Q2-Q4: Savings realization (+$XX,XXX)
- Net Year 1: $XX,XXX

### Year 2-3
[Steady-state savings projection]

## Risk-Adjusted Returns
- Best Case ROI: XXX%
- Expected Case ROI: XXX%
- Worst Case ROI: XXX%

## Comparison to Alternatives
| Scenario | 3-Year Cost | Opportunity Cost |
|----------|------------|------------------|
| **Do Nothing** | $XXX,XXX | High competitive risk |
| **Hire More Staff** | $XXX,XXX | Scales poorly |
| **Implement Automation** | $XX,XXX | **Best ROI** |

Use realistic numbers. Be conservative in estimates. Show sensitivity analysis.
"""
        
        try:
            response = self.ai.call_gemini(prompt)
            return response
        except Exception as e:
            return f"Error generating financial model: {e}"
    
    def generate_funding_application(self, company: str, research: dict, funding: dict):
        """Generate pre-filled funding application draft"""
        print("[PROPOSAL] Generating Funding Application Draft...")
        
        prompt = f"""
You are a grant writer preparing a funding application for {company}.

COMPANY RESEARCH:
{json.dumps(research, indent=2)[:2000]}

FUNDING OPPORTUNITIES:
{json.dumps(funding, indent=2)[:2000]}

Select the BEST MATCH funding program and create an application draft in MARKDOWN:

# Funding Application Draft: [Program Name]

## Applicant Information
**Company**: {company}
**Industry**: [From research]
**Employees**: [Estimate from research]
**Annual Revenue**: [Estimate or "Confidential"]

## Project Description
**Title**: [Compelling 10-word title]

**Summary** (150 words):
[Elevator pitch of the automation project]

**Problem Statement** (200 words):
[What business challenge this solves, using data from research]

**Proposed Solution** (300 words):
[Technical approach, deliverables, timeline]

**Innovation** (150 words):
[Why this is innovative for their industry]

## Budget Request
**Total Project Cost**: $XX,XXX
**Funding Requested**: $XX,XXX
**Company Co-Investment**: $XX,XXX

| Category | Amount | Justification |
|----------|--------|---------------|
| [Category 1] | $X,XXX | [Brief] |
| [Category 2] | $X,XXX | [Brief] |

## Expected Outcomes
**Quantitative**:
- [Metric 1]: X% improvement
- [Metric 2]: $XX,XXX savings
- [Metric 3]: XX hours saved

**Qualitative**:
- [Business impact 1]
- [Business impact 2]

## Timeline
- Month 1-2: [Phase 1]
- Month 3-4: [Phase 2]
- Month 5-6: [Phase 3]

## Team Qualifications
[Why InnovLead + their team can deliver]

## Sustainability
[How this continues providing value post-grant]

---

**Application Tips**:
- [Specific tip 1 for this grant]
- [Specific tip 2]
- [Required documentation]

Be specific and compelling. Use actual data from the research where possible.
"""
        
        try:
            response = self.ai.call_gemini(prompt)
            return response
        except Exception as e:
            return f"Error generating funding application: {e}"


def generate_full_proposal_suite(company_name: str, research_file: str = None, strategy_file: str = None, 
                                  funding_file: str = None, save_to_file: bool = True):
    """
    Generate complete proposal suite with all formats
    """
    print(f"\n{'='*60}")
    print(f"PROPOSAL SUITE GENERATION: {company_name}")
    print(f"{'='*60}\n")
    
    # Load input data
    base_path = os.path.dirname(__file__)
    
    # Load research
    if not research_file:
        research_file = os.path.join(base_path, f"../.tmp/research/{company_name.lower().replace(' ', '_')}_enhanced_research.json")
    
    if os.path.exists(research_file):
        with open(research_file, 'r') as f:
            research = json.load(f)
    else:
        print(f"[WARN] No research file found at {research_file}")
        research = {}
    
    # Load strategy
    if not strategy_file:
        strategy_file = os.path.join(base_path, f"../.tmp/strategy/{company_name.lower().replace(' ', '_')}_strategy.json")
    
    if os.path.exists(strategy_file):
        with open(strategy_file, 'r') as f:
            strategy = json.load(f)
    else:
        print(f"[WARN] No strategy file found at {strategy_file}")
        strategy = {}
    
    # Load funding
    if not funding_file:
        funding_file = os.path.join(base_path, f"../.tmp/funding/{company_name.lower().replace(' ', '_')}_funding.json")
    
    if os.path.exists(funding_file):
        with open(funding_file, 'r') as f:
            funding = json.load(f)
    else:
        print(f"[WARN] No funding file found at {funding_file}")
        funding = {}
    
    # Generate all proposals
    generator = ProposalSuiteGenerator()
    
    suite = {
        "company": company_name,
        "generated_at": datetime.now().isoformat(),
        "executive_summary": generator.generate_executive_summary(company_name, research, strategy, funding),
        "technical_roadmap": generator.generate_technical_roadmap(company_name, research, strategy),
        "financial_model": generator.generate_financial_model(company_name, strategy, funding),
        "funding_application": generator.generate_funding_application(company_name, research, funding)
    }
    
    # Save each format separately
    if save_to_file:
        output_dir = os.path.join(base_path, "../outputs/proposals")
        os.makedirs(output_dir, exist_ok=True)
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        company_slug = company_name.lower().replace(' ', '_')
        
        # Save Executive Summary
        exec_path = os.path.join(output_dir, f"{company_slug}_executive_summary_{date_str}.md")
        with open(exec_path, 'w', encoding='utf-8') as f:
            f.write(suite["executive_summary"])
        print(f"[SAVED] Executive Summary: {exec_path}")
        
        # Save Technical Roadmap
        tech_path = os.path.join(output_dir, f"{company_slug}_technical_roadmap_{date_str}.md")
        with open(tech_path, 'w', encoding='utf-8') as f:
            f.write(suite["technical_roadmap"])
        print(f"[SAVED] Technical Roadmap: {tech_path}")
        
        # Save Financial Model
        fin_path = os.path.join(output_dir, f"{company_slug}_financial_model_{date_str}.md")
        with open(fin_path, 'w', encoding='utf-8') as f:
            f.write(suite["financial_model"])
        print(f"[SAVED] Financial Model: {fin_path}")
        
        # Save Funding Application
        fund_path = os.path.join(output_dir, f"{company_slug}_funding_application_{date_str}.md")
        with open(fund_path, 'w', encoding='utf-8') as f:
            f.write(suite["funding_application"])
        print(f"[SAVED] Funding Application: {fund_path}")
        
        # Save complete suite as JSON
        suite_path = os.path.join(output_dir, f"{company_slug}_complete_suite_{date_str}.json")
        with open(suite_path, 'w', encoding='utf-8') as f:
            json.dump(suite, f, indent=2)
        print(f"[SAVED] Complete Suite: {suite_path}")
    
    return suite


if __name__ == "__main__":
    if len(sys.argv) > 1:
        company = sys.argv[1]
        
        suite = generate_full_proposal_suite(company)
        
        print("\n" + "="*60)
        print("PROPOSAL SUITE COMPLETE")
        print("="*60)
        print("\n4 stakeholder-specific documents generated:")
        print("  ✓ Executive Summary (C-Suite)")
        print("  ✓ Technical Roadmap (IT/Engineering)")
        print("  ✓ Financial Model (CFO)")
        print("  ✓ Funding Application (Grant Writer)")
        print("\n" + "="*60)
        
    else:
        print("Usage: python generate_proposal_suite.py 'Company Name'")
        print("\nPrerequisites:")
        print("  - Run research_enhanced.py first")
        print("  - Run generate_strategy.py")
        print("  - Run research_funding.py")
