"""
InnovLead Consultancy Proposal Generator
Interactive questionnaire-based proposal system that gathers client context
and generates persuasive, value-driven transformation proposals

Usage: python generate_consultancy_proposal.py
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json

class ConsultancyProposalGenerator:
    def __init__(self):
        self.client_data = {}
        self.output_dir = Path(__file__).parent.parent / "outputs" / "proposals"
        
    def gather_client_context(self):
        """Interactive questionnaire to understand client's situation"""
        
        print("\n" + "="*70)
        print("InnovLead Consultancy Proposal Generator")
        print("Gathering Context to Create Your Transformation Roadmap")
        print("="*70 + "\n")
        
        # SECTION 1: Basic Information
        print("📋 SECTION 1: Company Information\n")
        self.client_data['company_name'] = input("Company Name: ").strip()
        self.client_data['industry'] = input("Industry (e.g., Jewelry, E-commerce, Manufacturing): ").strip()
        self.client_data['years_in_business'] = input("Years in Business: ").strip()
        
        # SECTION 2: Current State Assessment
        print("\n" + "-"*70)
        print("📊 SECTION 2: Current State (Understanding Where You Are)")
        print("-"*70 + "\n")
        
        self.client_data['current_revenue'] = input("Current Annual Revenue (e.g., $500K): ").strip()
        self.client_data['team_size'] = input("Team Size (number of employees): ").strip()
        self.client_data['online_presence'] = input("Do you have an e-commerce website? (Yes/No/Basic): ").strip()
        
        print("\nWhat are your STRENGTHS? (comma-separated)")
        print("Examples: Quality craftsmanship, Loyal customers, Unique products, Strong brand")
        self.client_data['strengths'] = input("Strengths: ").strip()
        
        # SECTION 3: Pain Points & Challenges
        print("\n" + "-"*70)
        print("🎯 SECTION 3: Challenges (What's Holding You Back)")
        print("-"*70 + "\n")
        
        print("What are your BIGGEST CHALLENGES? (Select all that apply)")
        print("1. Limited online sales/reach")
        print("2. Too much manual/repetitive work")
        print("3. Ineffective marketing (wasted budget)")
        print("4. No data/analytics on customer behavior")
        print("5. Compliance concerns (PIPEDA, CASL, PCI)")
        print("6. Can't scale without hiring more people")
        print("7. Outdated technology/systems")
        print("8. Other")
        
        challenges_input = input("\nEnter challenge numbers (e.g., 1,2,4,5): ").strip()
        self.client_data['challenge_numbers'] = challenges_input
        
        if '8' in challenges_input:
            self.client_data['custom_challenge'] = input("Describe your custom challenge: ").strip()
        
        # SECTION 4: Goals & Aspirations
        print("\n" + "-"*70)
        print("🚀 SECTION 4: Goals (Where You Want to Be)")
        print("-"*70 + "\n")
        
        self.client_data['revenue_goal'] = input("Target Annual Revenue in 12 months (e.g., $1M): ").strip()
        self.client_data['main_goal'] = input("PRIMARY GOAL (e.g., Grow online sales, Automate operations, Expand nationally): ").strip()
        
        print("\nWhat would SUCCESS look like in 12 months?")
        self.client_data['success_vision'] = input("Success vision: ").strip()
        
        # SECTION 5: Decision Context
        print("\n" + "-"*70)
        print("💡 SECTION 5: Decision Context")
        print("-"*70 + "\n")
        
        self.client_data['budget_range'] = input("Investment Budget Range (e.g., $50K-150K, Flexible): ").strip()
        self.client_data['timeline'] = input("Desired Timeline to Start (e.g., Immediately, 30 days, Q1 2026): ").strip()
        self.client_data['decision_makers'] = input("Who's involved in the decision? (e.g., Owner, Board, CFO): ").strip()
        
        # SECTION 6: Specific Needs
        print("\n" + "-"*70)
        print("🔧 SECTION 6: Specific Needs (Optional - press Enter to skip)")
        print("-"*70 + "\n")
        
        self.client_data['specific_services'] = input("Any specific services needed? (e.g., SEO, Automation, App): ").strip()
        self.client_data['competitors'] = input("Key competitors to know about? ").strip()
        self.client_data['unique_value'] = input("What makes you different/special? ").strip()
        
        # Summary & Confirmation
        print("\n" + "="*70)
        print("📝 Context Gathered Successfully!")
        print("="*70)
        print(f"\nCompany: {self.client_data['company_name']}")
        print(f"Industry: {self.client_data['industry']}")
        print(f"Goal: {self.client_data['main_goal']}")
        print(f"Budget: {self.client_data['budget_range']}")
        
        confirm = input("\nGenerate proposal with this context? (Y/n): ").strip().lower()
        if confirm == 'n':
            print("Context gathering cancelled.")
            sys.exit(0)
            
        return self.client_data
    
    def analyze_challenges(self):
        """Identify specific gaps based on challenges selected"""
        challenge_map = {
            '1': {
                'name': 'Revenue Ceiling',
                'current': 'Limited by physical/local sales',
                'impact': 'Missing 60-80% of potential market',
                'solution': 'E-commerce Platform & Digital Marketing',
                'result': '3-5x revenue growth potential'
            },
            '2': {
                'name': 'Manual Inefficiency',
                'current': '30-50 hours/week on repetitive tasks',
                'impact': '$50-80K/year in wasted labor',
                'solution': 'Process Automation & AI Integration',
                'result': '90%+ time savings, scale without hiring'
            },
            '3': {
                'name': 'Marketing Blindness',
                'current': '50-70% wasted ad spend, no data',
                'impact': '$20-50K/year thrown away',
                'solution': 'Data Analytics & Optimization',
                'result': '3x better ROI, predictable growth'
            },
            '4': {
                'name': 'No Customer Intelligence',
                'current': 'Flying blind on customer behavior',
                'impact': 'Missing upsell, retention opportunities',
                'solution': 'CRM & Behavioral Analytics',
                'result': '40% higher customer lifetime value'
            },
            '5': {
                'name': 'Compliance Risk',
                'current': 'No PIPEDA/CASL/PCI framework',
                'impact': '$10K-$250K+ fine exposure',
                'solution': 'Built-in Compliance Infrastructure',
                'result': 'Zero violations, full protection'
            },
            '6': {
                'name': 'Scaling Bottleneck',
                'current': 'Growth limited by team capacity',
                'impact': 'Revenue capped, opportunities missed',
                'solution': 'Automation-First Architecture',
                'result': '10x capacity with same team'
            },
            '7': {
                'name': 'Technology Debt',
                'current': 'Outdated systems, manual processes',
                'impact': 'Slow, error-prone, expensive',
                'solution': 'Modern Tech Stack & Integration',
                'result': 'Fast, reliable, competitive'
            }
        }
        
        selected_challenges = []
        challenge_nums = self.client_data.get('challenge_numbers', '').split(',')
        
        for num in challenge_nums:
            num = num.strip()
            if num in challenge_map:
                selected_challenges.append(challenge_map[num])
        
        return selected_challenges[:4]  # Top 4 challenges for focused proposal
    
    def calculate_roi_projection(self):
        """Calculate projected ROI based on client data"""
        try:
            # Parse current revenue
            current_str = self.client_data.get('current_revenue', '500K').replace('$', '').replace(',', '').upper()
            if 'K' in current_str:
                current = float(current_str.replace('K', '')) * 1000
            elif 'M' in current_str:
                current = float(current_str.replace('M', '')) * 1000000
            else:
                current = float(current_str)
            
            # Calculate projections (conservative: 2x, moderate: 3x, aggressive: 5x)
            year1_revenue = current * 2
            year2_revenue = year1_revenue * 1.5
            year3_revenue = year2_revenue * 1.3
            
            # Format nicely
            def format_currency(amount):
                if amount >= 1000000:
                    return f"${amount/1000000:.1f}M"
                else:
                    return f"${amount/1000:.0f}K"
            
            return {
                'current': format_currency(current),
                'year1': format_currency(year1_revenue),
                'year2': format_currency(year2_revenue),
                'year3': format_currency(year3_revenue),
                'current_num': current,
                'year1_num': year1_revenue
            }
        except:
            # Default projections
            return {
                'current': '$500K',
                'year1': '$1M',
                'year2': '$1.8M',
                'year3': '$2.5M',
                'current_num': 500000,
                'year1_num': 1000000
            }
    
    def save_client_context(self):
        """Save client context for future reference"""
        company_slug = self.client_data['company_name'].lower().replace(' ', '_').replace('&', 'and')
        context_dir = self.output_dir / company_slug
        context_dir.mkdir(parents=True, exist_ok=True)
        
        context_file = context_dir / f"client_context_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(context_file, 'w') as f:
            json.dump(self.client_data, f, indent=2)
        
        print(f"\n✅ Client context saved: {context_file}")
        return context_dir
    
    def generate_html_proposal(self, challenges, roi_data, output_dir):
        """Generate consultancy-focused HTML proposal"""
        
        company = self.client_data['company_name']
        industry = self.client_data.get('industry', 'your industry')
        strengths_list = self.client_data.get('strengths', '').split(',')
        strengths_html = ''.join([f'<li>{s.strip()}</li>' for s in strengths_list if s.strip()])
        
        main_goal = self.client_data.get('main_goal', 'achieve digital transformation')
        success_vision = self.client_data.get('success_vision', 'operating at full digital capacity')
        
        # Build challenges section
        challenges_html = ''
        solutions_html = ''
        for i, ch in enumerate(challenges, 1):
            challenges_html += f'''
            <div class="challenge-card">
                <h4>Gap {i}: {ch['name']}</h4>
                <p><strong>Current State:</strong> {ch['current']}</p>
                <p><strong>Impact:</strong> {ch['impact']}</p>
            </div>'''
            
            solutions_html += f'''
            <div class="solution-card">
                <h4>{ch['name']} → Solution</h4>
                <p><strong>We Implement:</strong> {ch['solution']}</p>
                <p class="result-highlight"><strong>Your Result:</strong> {ch['result']}</p>
            </div>'''
        
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{company} - Digital Transformation Partnership</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #ffffff;
            line-height: 1.6;
        }}
        
        .slide {{
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 80px 100px;
            text-align: center;
            page-break-after: always;
            position: relative;
        }}
        
        h1 {{
            font-size: 5em;
            margin-bottom: 30px;
            background: linear-gradient(135deg, #FFD700, #FFA500);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            letter-spacing: -2px;
        }}
        
        h2 {{
            font-size: 3.5em;
            margin-bottom: 40px;
            color: #FFD700;
            font-weight: 700;
            text-shadow: 0 4px 20px rgba(255, 215, 0, 0.3);
        }}
        
        h3 {{
            font-size: 2.2em;
            margin: 30px 0 20px;
            color: #00D4FF;
            font-weight: 600;
        }}
        
        h4 {{
            font-size: 1.8em;
            margin: 15px 0;
            color: #FFD700;
        }}
        
        p, li {{
            font-size: 1.4em;
            line-height: 1.7;
            margin: 15px 0;
        }}
        
        .highlight {{
            color: #FFD700;
            font-weight: 700;
            font-size: 1.2em;
        }}
        
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            margin: 40px 0;
            width: 100%;
            max-width: 1400px;
        }}
        
        .challenge-card, .solution-card, .milestone-card {{
            background: linear-gradient(145deg, rgba(0, 212, 255, 0.12), rgba(0, 100, 150, 0.08));
            border: 2px solid rgba(0, 212, 255, 0.4);
            border-radius: 20px;
            padding: 35px;
            text-align: left;
            box-shadow: 0 10px 35px rgba(0, 212, 255, 0.2);
            transition: transform 0.3s;
        }}
        
        .challenge-card:hover, .solution-card:hover, .milestone-card:hover {{
            transform: translateY(-5px);
        }}
        
        .challenge-card::before, .solution-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #FFD700, #FFA500);
        }}
        
        .result-highlight {{
            color: #00FF00;
            font-weight: 700;
            font-size: 1.1em;
            margin-top: 15px;
        }}
        
        .stat-box {{
            background: linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(255, 165, 0, 0.1));
            border: 3px solid #FFD700;
            border-radius: 25px;
            padding: 50px 60px;
            margin: 30px;
            min-width: 300px;
            box-shadow: 0 15px 50px rgba(255, 215, 0, 0.4);
            transition: transform 0.3s;
        }}
        
        .stat-box:hover {{ transform: translateY(-8px); }}
        
        .stat-number {{
            font-size: 4em;
            font-weight: 800;
            color: #FFD700;
            text-shadow: 0 4px 15px rgba(255, 215, 0, 0.5);
        }}
        
        .stat-label {{
            font-size: 1.3em;
            color: #00D4FF;
            margin-top: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .roadmap-phase {{
            background: rgba(0, 212, 255, 0.1);
            border-left: 5px solid #00D4FF;
            padding: 30px;
            margin: 20px 0;
            border-radius: 10px;
            text-align: left;
        }}
        
        .accent-line {{
            width: 100px;
            height: 5px;
            background: linear-gradient(90deg, #FFD700, #FFA500);
            margin: 30px auto;
            border-radius: 5px;
        }}
        
        .slide-number {{
            position: absolute;
            bottom: 30px;
            right: 40px;
            font-size: 1.2em;
            color: rgba(255, 215, 0, 0.5);
        }}
        
        ul {{
            list-style: none;
            text-align: left;
            max-width: 900px;
            margin: 20px auto;
        }}
        
        ul li {{
            margin: 15px 0;
            padding-left: 40px;
            position: relative;
        }}
        
        ul li:before {{
            content: "→";
            position: absolute;
            left: 0;
            color: #FFD700;
            font-size: 1.5em;
            font-weight: bold;
        }}
        
        .cta-button {{
            display: inline-block;
            background: linear-gradient(135deg, #FFD700, #FFA500);
            color: #1a1a2e;
            padding: 25px 60px;
            border-radius: 50px;
            text-decoration: none;
            font-size: 1.6em;
            font-weight: 800;
            margin: 30px 0;
            box-shadow: 0 15px 40px rgba(255, 215, 0, 0.5);
            transition: transform 0.3s;
            text-transform: uppercase;
        }}
        
        .cta-button:hover {{
            transform: translateY(-8px) scale(1.05);
        }}
        
        @media print {{
            .slide {{ page-break-after: always; }}
        }}
    </style>
</head>
<body>

    <!-- SLIDE 1: Title - The Opportunity -->
    <div class="slide">
        <h1 style="font-size: 6em;">💎</h1>
        <h1>{company}</h1>
        <div class="accent-line"></div>
        <h3 style="font-size: 2.5em; color: #00D4FF;">Digital Transformation Partnership</h3>
        <p style="font-size: 1.8em; margin-top: 50px; font-weight: 300;">
            Unlocking Your Full Potential in the Digital Age
        </p>
        <p style="margin-top: 30px;">Presented by: <span class="highlight">William Meléndez Salas, MBA</span><br>InnovLead Canada Inc.</p>
        <div class="slide-number">1 / 9</div>
    </div>

    <!-- SLIDE 2: Your Current State -->
    <div class="slide">
        <h2>Understanding Where You Are Today</h2>
        <div class="accent-line"></div>
        <div class="grid-2">
            <div class="challenge-card">
                <h3>Your Strengths ✅</h3>
                <ul>
                    {strengths_html}
                    <li>Established in {industry}</li>
                    <li>Current revenue: {roi_data['current']}</li>
                </ul>
            </div>
            <div class="challenge-card">
                <h3>What's Missing 🎯</h3>
                <p style="font-size: 1.5em; margin: 20px 0;">
                    You have the foundation. Now it's time to <span class="highlight">multiply your reach</span> and <span class="highlight">eliminate inefficiencies</span> through digital transformation.
                </p>
                <p><strong>Your Goal:</strong> {main_goal}</p>
            </div>
        </div>
        <p style="font-size: 1.6em; margin-top: 50px; max-width: 1000px;">
            <strong>The Gap:</strong> You're operating at a fraction of your digital potential. Let's close that gap.
        </p>
        <div class="slide-number">2 / 9</div>
    </div>

    <!-- SLIDE 3: The Gaps We Identified -->
    <div class="slide">
        <h2>The Gaps Holding You Back</h2>
        <div class="accent-line"></div>
        <p style="font-size: 1.5em; margin-bottom: 40px;">Based on your situation, we identified these transformation opportunities:</p>
        <div class="grid-2">
            {challenges_html}
        </div>
        <p class="highlight" style="font-size: 1.8em; margin-top: 50px;">
            Each gap has a clear solution. Each solution drives measurable results.
        </p>
        <div class="slide-number">3 / 9</div>
    </div>

    <!-- SLIDE 4: How InnovLead Bridges Each Gap -->
    <div class="slide">
        <h2>How We Bridge Every Gap</h2>
        <div class="accent-line"></div>
        <div class="grid-2">
            {solutions_html}
        </div>
        <p style="font-size: 1.6em; margin-top: 50px; max-width: 1000px;">
            This isn't theory. These are proven systems we implement for you, customized to your business.
        </p>
        <div class="slide-number">4 / 9</div>
    </div>

    <!-- SLIDE 5: 90-Day Transformation Roadmap -->
    <div class="slide">
        <h2>Your 90-Day Transformation Path</h2>
        <div class="accent-line"></div>
        
        <div class="roadmap-phase">
            <h3>Days 1-30: Foundation 🏗️</h3>
            <ul>
                <li><strong>Week 1:</strong> Deep-dive discovery, strategy alignment</li>
                <li><strong>Week 2-4:</strong> Platform setup, automation infrastructure, compliance framework</li>
            </ul>
        </div>
        
        <div class="roadmap-phase">
            <h3>Days 31-60: Activation 🚀</h3>
            <ul>
                <li><strong>Week 5-6:</strong> Marketing launch, SEO optimization, content systems</li>
                <li><strong>Week 7-8:</strong> Team training, process automation, analytics dashboard</li>
            </ul>
        </div>
        
        <div class="roadmap-phase">
            <h3>Days 61-90: Optimization ⚡</h3>
            <ul>
                <li><strong>Week 9-10:</strong> Campaign launch, paid advertising, performance tracking</li>
                <li><strong>Week 11-12:</strong> A/B testing, conversion optimization, growth acceleration</li>
            </ul>
        </div>
        
        <p class="highlight" style="font-size: 1.8em; margin-top: 40px;">
            Day 91: Fully operational, first results flowing, ready to scale
        </p>
        <div class="slide-number">5 / 9</div>
    </div>

    <!-- SLIDE 6: What You'll Achieve -->
    <div class="slide">
        <h2>Your Success Milestones</h2>
        <div class="accent-line"></div>
        
        <div class="milestone-card" style="margin-bottom: 30px;">
            <h3>In 12 Months, You'll Have Achieved:</h3>
            <ul style="font-size: 1.3em;">
                <li>{success_vision}</li>
                <li>Revenue growth: {roi_data['current']} → {roi_data['year1']}</li>
                <li>90%+ reduction in manual work</li>
                <li>Full digital operations capability</li>
                <li>Scalable, profitable, predictable growth</li>
            </ul>
        </div>
        
        <div style="display: flex; gap: 30px; justify-content: center; flex-wrap: wrap;">
            <div class="stat-box">
                <div class="stat-number">{roi_data['year1']}</div>
                <div class="stat-label">Year 1 Revenue</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{roi_data['year2']}</div>
                <div class="stat-label">Year 2 Revenue</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{roi_data['year3']}</div>
                <div class="stat-label">Year 3 Revenue</div>
            </div>
        </div>
        
        <p class="highlight" style="font-size: 1.6em; margin-top: 40px;">
            From where you are to where you want to be - we build the bridge.
        </p>
        <div class="slide-number">6 / 9</div>
    </div>

    <!-- SLIDE 7: Investment & Value Return -->
    <div class="slide">
        <h2>Investment & Value Creation</h2>
        <div class="accent-line"></div>
        
        <div class="grid-2" style="margin-top: 50px;">
            <div class="stat-box">
                <div class="stat-label">Your Investment</div>
                <div class="stat-number" style="font-size: 3em;">$100-125K</div>
                <p style="margin-top: 20px;">After grants & tax credits</p>
            </div>
            <div class="stat-box">
                <div class="stat-label">Your Return (Year 1)</div>
                <div class="stat-number" style="font-size: 3em;">$250K+</div>
                <p style="margin-top: 20px;">Revenue growth + time saved + risk avoided</p>
            </div>
        </div>
        
        <div style="margin-top: 60px; text-align: left; max-width: 1000px;">
            <h3>What You Get:</h3>
            <ul style="font-size: 1.3em;">
                <li>Complete digital infrastructure</li>
                <li>Marketing automation systems</li>
                <li>Process automation (90%+ time savings)</li>
                <li>Compliance framework (zero violations)</li>
                <li>Analytics & optimization</li>
                <li>Ongoing strategic partnership</li>
            </ul>
        </div>
        
        <p class="highlight" style="font-size: 2em; margin-top: 50px;">
            ROI: 150-200% in Year 1 | Payback: 6-8 months
        </p>
        <div class="slide-number">7 / 9</div>
    </div>

    <!-- SLIDE 8: Why InnovLead -->
    <div class="slide">
        <h2>Why InnovLead Canada</h2>
        <div class="accent-line"></div>
        
        <div class="challenge-card" style="max-width: 900px; margin: 30px auto; text-align: center;">
            <h3 style="color: #FFD700;">William Meléndez Salas, MBA</h3>
            <p style="font-size: 1.2em; margin: 15px 0;">CEO & Principal – InnovLead Canada Inc.</p>
        </div>
        
        <div class="grid-2" style="margin-top: 40px;">
            <div class="milestone-card">
                <h4>Credentials</h4>
                <ul>
                    <li>ISO 27001 Lead Implementer</li>
                    <li>PIPEDA/CASL Compliance Expert</li>
                    <li>MBA in Big Data & PM</li>
                    <li>18% CAGR Quant Trader</li>
                    <li>10 years AI-led transformation</li>
                </ul>
            </div>
            <div class="milestone-card">
                <h4>What This Means for You</h4>
                <ul>
                    <li>Compliance-first (no liability)</li>
                    <li>Data-driven (every dollar optimized)</li>
                    <li>Hands-on (continuous improvement)</li>
                    <li>Partnership mindset (your success = our success)</li>
                </ul>
            </div>
        </div>
        
        <p class="highlight" style="font-size: 1.6em; margin-top: 50px;">
            We're not vendors. We're your strategic growth partners.
        </p>
        <div class="slide-number">8 / 9</div>
    </div>

    <!-- SLIDE 9: Your Path Forward -->
    <div class="slide">
        <h1 style="font-size: 4em;">Your Path Forward</h1>
        <div class="accent-line"></div>
        
        <div class="roadmap-phase" style="margin: 40px auto; max-width: 1000px;">
            <h3>Next Steps:</h3>
            <ul style="font-size: 1.3em;">
                <li><strong>Step 1:</strong> Discovery Session (90 minutes) - Deep-dive into your specific situation</li>
                <li><strong>Step 2:</strong> Custom Roadmap - Tailored transformation plan for {company}</li>
                <li><strong>Step 3:</strong> Funding Support - CDAP grants, SR&ED credits, financing options</li>
                <li><strong>Step 4:</strong> Kickoff (Day 21) - Begin your transformation journey</li>
            </ul>
        </div>
        
        <div style="margin: 60px 0;">
            <a href="mailto:wms090807@gmail.com" class="cta-button">Schedule Discovery Session</a>
        </div>
        
        <div class="challenge-card" style="display: inline-block; max-width: 700px;">
            <h4>Contact Information</h4>
            <p style="font-size: 1.2em;">
                <strong>William Meléndez Salas, MBA</strong><br>
                CEO & Principal – InnovLead Canada Inc.<br><br>
                📧 wms090807@gmail.com<br>
                🔗 linkedin.com/in/william-m-salas<br>
                📅 calendly.com/innovlead-ca
            </p>
        </div>
        
        <p style="margin-top: 60px; font-size: 1.5em; font-style: italic; font-weight: 300;">
            "Are you ready to unlock your company's full digital potential?"
        </p>
        
        <div class="slide-number">9 / 9</div>
    </div>

</body>
</html>'''
        
        # Save HTML
        company_slug = company.lower().replace(' ', '_').replace('&', 'and')
        filename = f"{company_slug}_transformation_proposal_{datetime.now().strftime('%Y%m%d')}.html"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n✅ HTML Proposal Generated!")
        print(f"📁 Saved to: {filepath}")
        print(f"\n🎯 Next Steps:")
        print(f"1. Open the HTML in Chrome/Edge")
        print(f"2. Press Ctrl+P to print")
        print(f"3. Save as PDF (Margins: None, Backgrounds: ON)")
        print(f"4. Send to {company}!")
        
        return filepath


def main():
    """Run consultancy proposal generator"""
    generator = ConsultancyProposalGenerator()
    
    # Gather context
    client_data = generator.gather_client_context()
    
    # Analyze challenges
    challenges = generator.analyze_challenges()
    
    # Calculate projections
    roi_data = generator.calculate_roi_projection()
    
    # Save context
    output_dir = generator.save_client_context()
    
    print("\n" + "="*70)
    print("🎯 Analysis Complete - Ready to Generate Proposal")
    print("="*70)
    print(f"\nIdentified {len(challenges)} Key Transformation Opportunities:")
    for i, challenge in enumerate(challenges, 1):
        print(f"{i}. {challenge['name']}")
    
    print(f"\nProjected Growth Path:")
    print(f"  Current: {roi_data['current']}")
    print(f"  Year 1: {roi_data['year1']}")
    print(f"  Year 2: {roi_data['year2']}")
    print(f"  Year 3: {roi_data['year3']}")
    
    print("\n📄 Generating HTML proposal...")
    
    # Generate HTML proposal
    html_path = generator.generate_html_proposal(challenges, roi_data, output_dir)
    
    print("\n" + "="*70)
    print("✅ PROPOSAL COMPLETE!")
    print("="*70)
    print(f"\n💎 Consultancy-Focused Transformation Proposal Generated")
    print(f"📁 Location: {html_path}")
    print(f"\n🚀 Ready to present to {client_data['company_name']}!")


if __name__ == "__main__":
    main()
