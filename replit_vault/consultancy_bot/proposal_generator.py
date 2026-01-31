"""
Template-Based Proposal Generator
Uses Jinja2 to generate professional proposals from templates

This replaces the hardcoded generate_jewelry_proposal_suite.py with a 
dynamic, template-driven system that works for any industry.
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from jinja2 import Environment, FileSystemLoader, Template


class ProposalGenerator:
    """Generate professional proposals from templates"""
    
    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize the proposal generator
        
        Args:
            template_dir: Path to templates directory (defaults to ./templates)
        """
        if template_dir is None:
            template_dir = os.path.join(os.path.dirname(__file__), "templates")
        
        self.template_dir = template_dir
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self.env.filters['format_currency'] = self._format_currency
        self.env.filters['format_date'] = self._format_date
        self.env.filters['format_percentage'] = self._format_percentage
    
    def _format_currency(self, value, currency='CAD'):
        """Format number as currency"""
        try:
            val = float(value)
            return f"${val:,.0f} {currency}"
        except (ValueError, TypeError):
            return value
    
    def _format_date(self, value, format='%B %d, %Y'):
        """Format date string"""
        if isinstance(value, str):
            try:
                dt = datetime.fromisoformat(value)
                return dt.strftime(format)
            except:
                return value
        elif isinstance(value, datetime):
            return value.strftime(format)
        return value
    
    def _format_percentage(self, value):
        """Format number as percentage"""
        try:
            val = float(value)
            return f"{val:.1f}%"
        except (ValueError, TypeError):
            return value
    
    def generate_executive_summary(
        self,
        company_name: str,
        industry: str,
        strategy_data: Dict,
        competitor_data: Dict,
        funding_data: Optional[Dict] = None,
        custom_data: Optional[Dict] = None
    ) -> str:
        """
        Generate an executive summary proposal
        
        Args:
            company_name: Name of the client company
            industry: Industry sector
            strategy_data: Strategy analysis from generate_strategy.py
            competitor_data: Competitor research from competitor_research.py
            funding_data: Optional funding opportunities data
            custom_data: Optional additional custom data for the template
            
        Returns:
            Rendered markdown proposal
        """
        template = self.env.get_template('executive_summary.md')
        
        # Prepare template context
        context = {
            'company_name': company_name,
            'industry': industry,
            'date': datetime.now(),
            'strategy': strategy_data,
            'competitors': competitor_data,
            'funding': funding_data or {},
            'innovlead': {
                'contact': {
                    'name': 'William Meléndez Salas, MBA',
                    'title': 'CEO & Principal',
                    'company': 'InnovLead Canada Inc.',
                    'email': 'wms090807@gmail.com',
                    'linkedin': 'linkedin.com/in/william-m-salas'
                },
                'credentials': [
                    'ISO 27001 Lead Implementer',
                    'PIPEDA, Loi 25, CASL Compliance Expert',
                    'MBA in Big Data & Project Management',
                    '10× Colombian Judo Champion',
                    'Quant Trader (18% CAGR)',
                    '6-time Published Author'
                ]
            }
        }
        
        # Merge custom data
        if custom_data:
            context.update(custom_data)
        
        # Render template
        rendered = template.render(**context)
        return rendered
    
    def generate_technical_roadmap(
        self,
        company_name: str,
        strategy_data: Dict,
        timeline_months: int = 12
    ) -> str:
        """
        Generate a technical implementation roadmap
        
        Args:
            company_name: Name of the client company
            strategy_data: Strategy analysis with technical recommendations
            timeline_months: Implementation timeline in months
        """
        try:
            template = self.env.get_template('technical_roadmap.md')
        except:
            # If template doesn't exist, return a placeholder
            return self._generate_basic_roadmap(company_name, strategy_data, timeline_months)
        
        context = {
            'company_name': company_name,
            'date': datetime.now(),
            'strategy': strategy_data,
            'timeline_months': timeline_months
        }
        
        return template.render(**context)
    
    def generate_financial_model(
        self,
        company_name: str,
        strategy_data: Dict,
        funding_data: Optional[Dict] = None,
        years: int = 3
    ) -> str:
        """
        Generate a financial projection model
        
        Args:
            company_name: Name of the client company
            strategy_data: Strategy with ROI estimates
            funding_data: Optional funding opportunities
            years: Number of years to project
        """
        try:
            template = self.env.get_template('financial_model.md')
        except:
            return self._generate_basic_financial(company_name, strategy_data, years)
        
        context = {
            'company_name': company_name,
            'date': datetime.now(),
            'strategy': strategy_data,
            'funding': funding_data or {},
            'years': years
        }
        
        return template.render(**context)
    
    def _generate_basic_roadmap(self, company_name: str, strategy_data: Dict, months: int) -> str:
        """Generate a basic roadmap when template is missing"""
        content = f"# Technical Roadmap - {company_name}\n\n"
        content += f"**Date**: {datetime.now().strftime('%B %d, %Y')}\n"
        content += f"**Timeline**: {months} months\n\n"
        content += "## Implementation Phases\n\n"
        
        if 'opportunities' in strategy_data:
            for idx, opp in enumerate(strategy_data['opportunities'][:3], 1):
                content += f"### Phase {idx}: {opp.get('title', 'Implementation Phase')}\n"
                content += f"**Objective**: {opp.get('pain_point', 'Address business challenge')}\n"
                content += f"**Solution**: {opp.get('proposed_solution', 'Technical implementation')}\n"
                content += f"**Impact**: {opp.get('roi_impact', 'Business value')}\n\n"
        
        return content
    
    def _generate_basic_financial(self, company_name: str, strategy_data: Dict, years: int) -> str:
        """Generate basic financial projection when template is missing"""
        content = f"# Financial Projections - {company_name}\n\n"
        content += f"**Date**: {datetime.now().strftime('%B %d, %Y')}\n"
        content += f"**Projection Period**: {years} years\n\n"
        content += "## Investment Summary\n\n"
        content += "### Expected ROI\n\n"
        
        if 'opportunities' in strategy_data:
            for opp in strategy_data['opportunities']:
                content += f"- **{opp.get('title', 'Opportunity')}**: {opp.get('roi_impact', 'TBD')}\n"
        
        return content
    
    def save_proposal(self, content: str, company_name: str, proposal_type: str = "executive_summary") -> str:
        """
        Save proposal to file
        
        Args:
            content: Rendered proposal content
            company_name: Client company name
            proposal_type: Type of proposal (executive_summary, technical_roadmap, etc.)
            
        Returns:
            Path to saved file
        """
        output_dir = os.path.join(
            os.path.dirname(__file__), 
            "../storage/proposals",
            company_name.lower().replace(' ', '_')
        )
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = f"{company_name.lower().replace(' ', '_')}_{proposal_type}_{timestamp}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[SUCCESS] Proposal saved to: {filepath}")
        return filepath


def generate_proposal(
    company_name: str,
    industry: str,
    strategy_file: Optional[str] = None,
    competitor_file: Optional[str] = None,
    funding_file: Optional[str] = None,
    proposal_type: str = "executive_summary",
    save_to_file: bool = True
) -> str:
    """
    Main function to generate proposals from data files
    
    Args:
        company_name: Name of the client company
        industry: Industry sector
        strategy_file: Path to strategy JSON file
        competitor_file: Path to competitor research JSON file
        funding_file: Path to funding research JSON file
        proposal_type: Type of proposal to generate
        save_to_file: Whether to save to file
    """
    generator = ProposalGenerator()
    
    # Load data from files
    strategy_data = {}
    competitor_data = {}
    funding_data = {}
    
    if strategy_file and os.path.exists(strategy_file):
        with open(strategy_file, 'r', encoding='utf-8') as f:
            strategy_data = json.load(f)
    
    if competitor_file and os.path.exists(competitor_file):
        with open(competitor_file, 'r', encoding='utf-8') as f:
            competitor_data = json.load(f)
    
    if funding_file and os.path.exists(funding_file):
        with open(funding_file, 'r', encoding='utf-8') as f:
            funding_data = json.load(f)
    
    # Generate appropriate proposal
    if proposal_type == "executive_summary":
        content = generator.generate_executive_summary(
            company_name, 
            industry, 
            strategy_data, 
            competitor_data, 
            funding_data
        )
    elif proposal_type == "technical_roadmap":
        content = generator.generate_technical_roadmap(company_name, strategy_data)
    elif proposal_type == "financial_model":
        content = generator.generate_financial_model(company_name, strategy_data, funding_data)
    else:
        raise ValueError(f"Unknown proposal type: {proposal_type}")
    
    # Save to file
    if save_to_file:
        generator.save_proposal(content, company_name, proposal_type)
    
    return content


if __name__ == "__main__":
    if len(sys.argv) > 2:
        company = sys.argv[1]
        industry = sys.argv[2]
        proposal_type = sys.argv[3] if len(sys.argv) > 3 else "executive_summary"
        
        # Try to find data files in default locations
        base_dir = os.path.dirname(__file__)
        company_slug = company.lower().replace(' ', '_')
        
        strategy_file = os.path.join(base_dir, f"../storage/consultancy/strategy/{company_slug}_strategy.json")
        competitor_file = os.path.join(base_dir, f"../storage/consultancy/competitor_research/{company_slug}_competitors.json")
        funding_file = os.path.join(base_dir, f"../storage/consultancy/funding/{company_slug}_funding.json")
        
        content = generate_proposal(
            company, 
            industry,
            strategy_file if os.path.exists(strategy_file) else None,
            competitor_file if os.path.exists(competitor_file) else None,
            funding_file if os.path.exists(funding_file) else None,
            proposal_type
        )
        
        print("\n" + "="*60)
        print(f"Proposal generated for {company}")
        print("="*60)
        
    else:
        print("Usage: python proposal_generator.py 'Company Name' 'Industry' [proposal_type]")
        print("Example: python proposal_generator.py 'TechCorp' 'SaaS' executive_summary")
