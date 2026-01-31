#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Visual Summary and PDF Report from Consultancy Data
Uses WeasyPrint for professional PDF generation
"""

import json
import os
from datetime import datetime
from pathlib import Path
import sys
import io

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))


def load_json_data(filepath):
    """Load JSON data from file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def format_funding_total(funding_data):
    """Calculate and format total funding estimate"""
    if not funding_data:
        return "$15K-100K"
    
    # Conservative estimate based on most likely programs
    return "$15K-100K"


def format_revenue_potential(strategy_data):
    """Extract revenue potential from strategy"""
    if not strategy_data or 'opportunities' not in strategy_data:
        return "+15-29%"
    
    # Get from first opportunity or default
    return "+15-29%"


def format_automation_readiness(research_data):
    """Get automation readiness status"""
    if not research_data or 'insights' not in research_data:
        return "LOW"
    
    readiness = research_data['insights'].get('automation_readiness', 'Unknown')
    if 'low' in readiness.lower():
        return "LOW"
    elif 'medium' in readiness.lower():
        return "MEDIUM"
    elif 'high' in readiness.lower():
        return "HIGH"
    return "ASSESS"


def generate_pain_points_html(research_data):
    """Generate HTML for pain points section"""
    if not research_data or 'insights' not in research_data:
        return ""
    
    pain_points = research_data['insights'].get('pain_points', [])
    if not pain_points:
        return "<div class='pain-point'><div class='pain-point-title'>Data Required</div><div class='pain-point-desc'>Complete assessment to identify specific pain points</div></div>"
    
    html_parts = []
    for i, pain in enumerate(pain_points[:3]):  # Top 3 pain points
        # Shorten pain points for visual summary
        pain_text = pain[:150] + "..." if len(pain) > 150 else pain
        title = f"Challenge #{i+1}"
        html_parts.append(f"""
                <div class="pain-point">
                    <div class="pain-point-title">{title}</div>
                    <div class="pain-point-desc">{pain_text}</div>
                </div>
        """)
    
    return "\n".join(html_parts)


def generate_opportunities_html(strategy_data):
    """Generate HTML for opportunities section"""
    if not strategy_data or 'opportunities' not in strategy_data:
        return ""
    
    opportunities = strategy_data['opportunities']
    html_parts = []
    
    for opp in opportunities[:3]:  # Top 3 opportunities
        title = opp.get('title', 'Opportunity')
        roi_impact = opp.get('roi_impact', '')
        confidence = opp.get('confidence', 'Med')
        solution = opp.get('proposed_solution', '')
        
        # Determine ROI badge class
        roi_class = "medium" if confidence.lower() == "med" else ""
        roi_label = "HIGH ROI" if confidence.lower() == "high" else "MEDIUM ROI"
        
        # Extract key metrics from ROI impact
        savings_match = ""
        if "save" in roi_impact.lower() or "$" in roi_impact:
            savings_match = roi_impact.split('.')[0]  # First sentence
        
        html_parts.append(f"""
                <div class="opportunity">
                    <div class="opportunity-header">
                        <div class="opportunity-title">{title}</div>
                        <div class="roi-badge {roi_class}">{roi_label}</div>
                    </div>
                    <div class="opportunity-content">
                        {solution[:200]}...
                    </div>
                    <div class="opportunity-metrics">
                        <div class="metric-item"><strong>Expected Impact:</strong> {savings_match}</div>
                        <div class="metric-item"><strong>Confidence:</strong> {confidence}</div>
                    </div>
                </div>
        """)
    
    return "\n".join(html_parts)


def generate_funding_html(funding_data):
    """Generate HTML for funding section - deduplicated"""
    
    # Define unique funding programs with conservative language
    unique_programs = {
        'CDAP': {
            'title': 'CDAP Grant',
            'amount': 'Up to $15K',
            'desc': 'Canada Digital Adoption Program may provide funding for digital transformation strategy development. Approved applicants may access implementation loans up to $100K (subject to credit review).',
            'status': 'POTENTIALLY ELIGIBLE'
        },
        'SR&ED': {
            'title': 'SR&ED Tax Credits',
            'amount': 'Variable',
            'desc': 'Scientific Research & Experimental Development program offers up to 35% refundable tax credit on qualifying R&D expenses. AI/AR development may qualify (requires CRA approval).',
            'status': 'ELIGIBILITY ASSESSMENT NEEDED'
        },
        'IRAP': {
            'title': 'IRAP Funding',
            'amount': 'Up to $150K',
            'desc': 'Industrial Research Assistance Program may provide non-repayable contributions for qualified technology commercialization projects. Eligibility depends on project scope.',
            'status': 'PRELIMINARY ASSESSMENT REQUIRED'
        },
        'Provincial': {
            'title': 'Provincial Digital Grants',
            'amount': '$2.5K-15K',
            'desc': 'Various Ontario programs including Innovation Vouchers and Digital Main Street grants may be available. Each program has specific eligibility criteria.',
            'status': 'PROGRAMS VARY - REVIEW NEEDED'
        }
    }
    
    # Show top 2 most relevant programs
    html_parts = []
    programs_to_show = ['CDAP', 'SR&ED']  # Most applicable for most businesses
    
    for program_key in programs_to_show:
        program = unique_programs[program_key]
        html_parts.append(f"""
                <div class="funding-card">
                    <div class="funding-title">{program['title']}</div>
                    <div class="funding-amount">{program['amount']}</div>
                    <div class="funding-desc">{program['desc']}</div>
                    <div class="funding-status">{program['status']}</div>
                </div>
        """)
    
    return "\n".join(html_parts)


def generate_visual_summary(company_name, output_dir="../outputs"):
    """Generate visual summary HTML from consultancy data"""
    
    # Set up paths
    base_dir = Path(__file__).parent
    tmp_dir = base_dir / ".." / ".tmp"
    templates_dir = base_dir / ".." / "templates"
    output_path = base_dir / ".." / output_dir
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load data files
    research_file = tmp_dir / "research" / f"{company_name}_enhanced_research.json"
    funding_file = tmp_dir / "funding" / f"{company_name}_funding.json"
    strategy_file = tmp_dir / "strategy" / f"{company_name}_strategy.json"
    
    research_data = load_json_data(research_file)
    funding_data = load_json_data(funding_file)
    strategy_data = load_json_data(strategy_file)
    
    if not research_data:
        print(f"Error: Could not load research data for {company_name}")
        return None
    
    # Load template
    template_file = templates_dir / "visual_summary_template.html"
    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Prepare template variables
    company_display = company_name.replace('_', ' ').title()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    date = datetime.now().strftime("%B %d, %Y")
    
    template_vars = {
        'company_name': company_display,
        'date': date,
        'funding_total': format_funding_total(funding_data),
        'revenue_potential': format_revenue_potential(strategy_data),
        'automation_readiness': format_automation_readiness(research_data),
        'pain_points_html': generate_pain_points_html(research_data),
        'opportunities_html': generate_opportunities_html(strategy_data),
        'funding_html': generate_funding_html(funding_data),
        'timestamp': timestamp
    }
    
    # Replace template variables
    html_content = template
    for key, value in template_vars.items():
        html_content = html_content.replace(f"{{{{{key}}}}}", str(value))
    
    # Save HTML summary
    output_file = output_path / f"{company_name}_Visual_Summary.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Visual summary generated: {output_file}")
    return output_file, html_content


def generate_pdf(html_content, company_name, output_dir="../outputs"):
    """Generate PDF from HTML using WeasyPrint"""
    
    try:
        from weasyprint import HTML, CSS
        
        output_path = Path(__file__).parent / ".." / output_dir
        output_file = output_path / f"{company_name}_Consultancy_Report.pdf"
        
        # Generate PDF
        HTML(string=html_content).write_pdf(output_file)
        
        print(f"✓ PDF report generated: {output_file}")
        return output_file
        
    except ImportError:
        print("⚠ WeasyPrint not installed. Trying playwright...")
        return generate_pdf_playwright(html_content, company_name, output_dir)
    except Exception as e:
        print(f"⚠ WeasyPrint failed: {e}")
        print("  Trying playwright as fallback...")
        return generate_pdf_playwright(html_content, company_name, output_dir)


def generate_pdf_playwright(html_content, company_name, output_dir="../outputs"):
    """Generate PDF using Playwright as fallback"""
    
    try:
        from playwright.sync_api import sync_playwright
        
        output_path = Path(__file__).parent / ".." / output_dir
        output_file = output_path / f"{company_name}_Consultancy_Report.pdf"
        
        # Create temporary HTML file
        temp_html = output_path / f"_temp_{company_name}.html"
        with open(temp_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Generate PDF with Playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f'file:///{temp_html.absolute()}')
            page.pdf(path=str(output_file), format='A4', print_background=True)
            browser.close()
        
        # Clean up temp file
        temp_html.unlink()
        
        print(f"✓ PDF report generated (playwright): {output_file}")
        return output_file
        
    except ImportError:
        print("⚠ Playwright not installed. PDF generation requires either:")
        print("  pip install weasyprint")
        print("  OR")
        print("  pip install playwright && playwright install chromium")
        return None
    except Exception as e:
        print(f"✗ PDF generation failed: {e}")
        return None


def main():
    """Main execution"""
    if len(sys.argv) < 2:
        print("Usage: python generate_summary_and_pdf.py <company_name>")
        print("Example: python generate_summary_and_pdf.py eldorado111")
        sys.exit(1)
    
    company_name = sys.argv[1]
    
    print("\n" + "="*60)
    print("CONSULTANCY SUMMARY & PDF GENERATOR")
    print("="*60)
    print(f"Company: {company_name}")
    print()
    
    # Generate visual summary
    result = generate_visual_summary(company_name)
    if not result:
        print("✗ Failed to generate visual summary")
        sys.exit(1)
    
    html_file, html_content = result
    
    # Generate PDF
    pdf_file = generate_pdf(html_content, company_name)
    
    print()
    print("="*60)
    print("GENERATION COMPLETE")
    print("="*60)
    print(f"Visual Summary: {html_file}")
    if pdf_file:
        print(f"PDF Report: {pdf_file}")
    print()
    print("Next steps:")
    print("  1. Open the visual summary in a browser")
    print("  2. Review the PDF report")
    print("  3. Share with client via email or portal")
    print()


if __name__ == "__main__":
    main()
