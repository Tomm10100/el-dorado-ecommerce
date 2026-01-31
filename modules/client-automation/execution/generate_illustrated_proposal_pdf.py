"""
Automated Illustrated Proposal PDF Generator
Generates professional PDFs with custom AI-generated illustrations using KeiAI

Usage: python generate_illustrated_proposal_pdf.py "El Dorado Gold and Silver"
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
import time

load_dotenv()

# Configuration
KEI_AI_API_KEY = os.getenv("KEI_AI_API_KEY", "")
KEI_AI_BASE_URL = "https://api.kie.ai/api/v1"
KEI_AI_TASK_URL = f"{KEI_AI_BASE_URL}/jobs/createTask"
KEI_AI_QUERY_URL = f"{KEI_AI_BASE_URL}/jobs/recordInfo"

class IllustratedProposalGenerator:
    def __init__(self, company_name: str):
        self.company_name = company_name
        self.company_slug = company_name.lower().replace(' ', '_').replace('&', 'and')
        self.output_dir = Path(__file__).parent.parent / "outputs" / "proposals" / self.company_slug
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_images_dir = self.output_dir / "illustrations"
        self.temp_images_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_illustration(self, prompt: str, filename: str) -> Path:
        """Generate custom illustration using KeiAI"""
        print(f"Generating illustration: {filename}...")
        
        if not KEI_AI_API_KEY:
            print("  No KeiAI API key - skipping illustration")
            return None
        
        try:
            # Create task with improved negative prompts for text
            has_text = "text reading" in prompt.lower() or "exactly" in prompt.lower()
            
            if has_text:
                negative_prompt = ("blurry, low quality, distorted, misspelled, wrong spelling, "
                                 "illegible text, fuzzy letters, distorted letters, jumbled text, "
                                 "wrong words, extra characters, poor typography")
            else:
                negative_prompt = "blurry, low quality, distorted"
            
            payload = {
                "model": "google/imagen4",  # Best for text and icons
                "input": {
                    "prompt": prompt,
                    "aspect_ratio": "16:9",  # Good for presentation slides
                    "num_images": "1",
                    "negative_prompt": negative_prompt
                }
            }
            
            response = requests.post(
                KEI_AI_TASK_URL,
                json=payload,
                headers={
                    "Authorization": f"Bearer {KEI_AI_API_KEY}",
                    "Content-Type": "application/json"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 200:
                    task_id = data.get("data", {}).get("taskId")
                    print(f"  Task ID: {task_id}")
                    
                    # Poll for completion
                    image_url = self.wait_for_image(task_id)
                    
                    if image_url:
                        # Download image
                        image_path = self.temp_images_dir / f"{filename}.png"
                        img_response = requests.get(image_url, timeout=30)
                        
                        if img_response.status_code == 200:
                            with open(image_path, 'wb') as f:
                                f.write(img_response.content)
                            print(f"  Illustration saved: {filename}")
                            return image_path
            
            print(f"  Could not generate illustration")
            return None
            
        except Exception as e:
            print(f"  Error generating illustration: {e}")
            return None
    
    def wait_for_image(self, task_id: str, max_wait: int = 120) -> str:
        """Poll task until complete"""
        start_time = time.time()
        
        while (time.time() - start_time) < max_wait:
            try:
                response = requests.get(
                    f"{KEI_AI_QUERY_URL}?taskId={task_id}",
                    headers={"Authorization": f"Bearer {KEI_AI_API_KEY}"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == 200:
                        task_data = data.get("data", {})
                        state = task_data.get("state")
                        
                        if state == "success":
                            result_json_str = task_data.get("resultJson", "{}")
                            result_json = json.loads(result_json_str)
                            result_urls = result_json.get("resultUrls", [])
                            if result_urls:
                                return result_urls[0]
                        elif state == "fail":
                            return None
                        
                time.sleep(5)
            except:
                time.sleep(5)
        
        return None
    
    def create_pdf(self):
        """Generate illustrated PDF proposal"""
        print(f"\nGenerating PDF for {self.company_name}...\n")
        
        pdf_filename = self.output_dir / f"{self.company_slug}_illustrated_proposal_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        # Generate illustrations with HYBRID APPROACH (v3)
        # - Simple text (1-2 words): Include in AI image
        # - Complex data: Text-free, add in PDF
        
        # Check if this is v3 (hybrid) generation
        use_hybrid = "v3" in self.company_slug or "hybrid" in self.company_slug
        
        if use_hybrid:
            print("Using HYBRID approach (text-in-AI for simple elements)\n")
            illustrations = {
                "market_opportunity": self.generate_illustration(
                    "Large bold text reading exactly 'GROWTH' in gold metallic color (#FFD700), "
                    "centered composition, modern sans-serif typeface, sharp typography, "
                    "upward pointing arrow behind text, blue gradient background, "
                    "professional minimalist style, ultra-sharp letters, high contrast",
                    "market_opportunity"
                ),
                "competitive_advantage": self.generate_illustration(
                    "Text reading exactly 'WINNER' in large bold gold letters (#FFD700), "
                    "gold trophy icon below text, centered composition, "
                    "modern bold typeface, sharp edges, blue accent elements, "
                    "professional clean design, perfect letter spacing",
                    "competitive_advantage"
                ),
                "technology_stack": self.generate_illustration(
                    "Connected network of abstract tech icons, circular nodes linked by flowing lines, "
                    "gold and blue color palette, clean minimalist style, no text, "
                    "geometric shapes, modern professional design",
                    "technology_stack"
                ),
                "growth_trajectory": self.generate_illustration(
                    "Large bold text reading exactly 'ROI' in gold color (#FFD700), "
                    "upward trending arrow integrated with letters, "
                    "modern bold sans-serif font, sharp typography, "
                    "blue to gold gradient background, professional style, "
                    "perfect letter spacing, ultra-sharp rendering",
                    "growth_trajectory"
                )
            }
        else:
            print("Using TEXT-FREE approach (no text in AI images)\n")
            illustrations = {
                "market_opportunity": self.generate_illustration(
                    "Abstract geometric arrow pointing upward, clean minimalist design, "
                    "gold gradient flowing into deep blue, smooth curves, professional modern icon style, "
                    "no text, no labels, no numbers, simple shapes only",
                    "market_opportunity"
                ),
                "competitive_advantage": self.generate_illustration(
                    "Gold trophy icon in center, surrounded by clean checkmark symbols arranged in circle, "
                    "minimalist flat design, blue accent elements, no text, no labels, "
                    "simple geometric shapes, professional modern style",
                    "competitive_advantage"
                ),
                "technology_stack": self.generate_illustration(
                    "Connected network of abstract tech icons, circular nodes linked by flowing lines, "
                    "gold and blue color palette, clean minimalist style, no text, "
                    "geometric shapes, modern professional design",
                    "technology_stack"
                ),
                "growth_trajectory": self.generate_illustration(
                    "Smooth curved arrow rising exponentially upward, gold coin icons scattered along path, "
                    "blue to gold gradient, clean modern design, no text, no numbers, "
                    "no labels, simple elegant visualization",
                    "growth_trajectory"
                )
            }
        
        # Create PDF
        doc = SimpleDocTemplate(
            str(pdf_filename),
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=0.75*inch
        )
        
        # Container for flowables
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=32,
            textColor=colors.HexColor('#FFD700'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#00D4FF'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=20,
            textColor=colors.HexColor('#FFD700'),
            spaceAfter=15,
            spaceBefore=20
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            leading=16,
            spaceAfter=12
        )
        
        highlight_style = ParagraphStyle(
            'HighlightBox',
            parent=styles['BodyText'],
            fontSize=14,
            textColor=colors.HexColor('#FFD700'),
            leading=20,
            leftIndent=20,
            rightIndent=20,
            spaceAfter=15,
            spaceBefore=15,
            borderColor=colors.HexColor('#FFD700'),
            borderWidth=2,
            borderPadding=15
        )
        
        # SLIDE 1: Title Page
        story.append(Spacer(1, 2*inch))
        story.append(Paragraph("💎", title_style))
        story.append(Paragraph(self.company_name, title_style))
        story.append(Paragraph("Strategic Partnership Proposal", subtitle_style))
        story.append(Spacer(1, 0.5*inch))
        
        # Key metrics boxes
        metrics_data = [
            ["$440K", "$94-101K", "160-188%"],
            ["Year 1 Revenue", "Net Investment", "ROI"]
        ]
        
        metrics_table = Table(metrics_data, colWidths=[2*inch, 2*inch, 2*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFD700')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 24),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#00D4FF')),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.white),
            ('FONTSIZE', (0, 1), (-1, 1), 11),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#FFD700'))
        ]))
        
        story.append(metrics_table)
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph("Presented by: <b>William Meléndez Salas, MBA</b><br/>InnovLead Canada Inc.", 
                              ParagraphStyle('presenter', parent=body_style, alignment=TA_CENTER)))
        
        story.append(PageBreak())
        
        # SLIDE 2: Market Opportunity
        story.append(Paragraph("The Market Opportunity", heading_style))
        
        if illustrations["market_opportunity"] and illustrations["market_opportunity"].exists():
            img = Image(str(illustrations["market_opportunity"]), width=6*inch, height=3.375*inch)
            story.append(img)
            story.append(Spacer(1, 0.2*inch))
        
        market_data = [
            ["Metric", "Value"],
            ["Canadian Jewelry Market", "$4.2B CAD"],
            ["Silver & Gold Segment", "$680M"],
            ["Online Penetration", "22% and growing"],
            ["Target Market", "$150M+ addressable"]
        ]
        
        market_table = Table(market_data, colWidths=[3*inch, 3*inch])
        market_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFD700')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8)
        ]))
        
        story.append(market_table)
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(
            "<b>The Canadian gold and silver jewelry market is growing at 6.2% annually "
            "with accelerating online adoption. Perfect timing to enter.</b>",
            highlight_style
        ))
        
        story.append(PageBreak())
        
        # SLIDE 3: The Market Gap
        story.append(Paragraph("Why We Win: The Market Gap", heading_style))
        
        if illustrations["competitive_advantage"] and illustrations["competitive_advantage"].exists():
            img = Image(str(illustrations["competitive_advantage"]), width=6*inch, height=3.375*inch)
            story.append(img)
            story.append(Spacer(1, 0.2*inch))
        
        gap_data = [
            ["What Market Wants", "Who Delivers It?", f"{self.company_name}"],
            ["Professional Quality", "✅ Mejuri (expensive)\n❌ Etsy (inconsistent)", "✅ YES"],
            ["Personal Touch", "✅ Etsy\n❌ Amazon, Mejuri", "✅ YES"],
            ["Fair Pricing", "✅ Amazon\n❌ Mejuri, Brilliant Earth", "✅ YES"],
            ["Modern Technology", "✅ Mejuri, Amazon\n❌ Etsy, People's", "✅ YES"]
        ]
        
        gap_table = Table(gap_data, colWidths=[2*inch, 2.5*inch, 1.5*inch])
        gap_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFD700')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#FFD700')),
            ('BACKGROUND', (2, 1), (2, -1), colors.HexColor('#00FF00')),
            ('TEXTCOLOR', (2, 1), (2, -1), colors.black),
            ('FONTNAME', (2, 1), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (2, 1), (2, -1), 14),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10)
        ]))
        
        story.append(gap_table)
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(
            f"<b>Nobody has all four. This is {self.company_name}'s position.</b>",
            highlight_style
        ))
        
        story.append(PageBreak())
        
        # SLIDE 4: Partnership Structure
        story.append(Paragraph("The Partnership Structure", heading_style))
        
        partnership_text = f"""
        <b>{self.company_name} Focuses On:</b><br/>
        💎 Production excellence &amp; craftsmanship<br/>
        💎 Quality control &amp; artisan work<br/>
        💎 Inventory management<br/>
        💎 Shipping &amp; fulfillment<br/>
        <br/>
        <b>InnovLead Delivers:</b><br/>
        🚀 Complete e-commerce platform<br/>
        🚀 Marketing automation (email, SMS, social)<br/>
        🚀 SEO &amp; content strategy<br/>
        🚀 Process automation ($60K/year savings)<br/>
        🚀 PIPEDA/CASL/PCI compliance<br/>
        🚀 Paid advertising &amp; growth marketing<br/>
        🚀 Data analytics &amp; optimization
        """
        
        story.append(Paragraph(partnership_text, body_style))
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(
            "<b>You focus on craft. We handle everything digital.</b>",
            highlight_style
        ))
        
        story.append(PageBreak())
        
        # SLIDE 5: Financial Overview
        story.append(Paragraph("The Numbers That Matter", heading_style))
        
        if illustrations["growth_trajectory"] and illustrations["growth_trajectory"].exists():
            img = Image(str(illustrations["growth_trajectory"]), width=6*inch, height=3.375*inch)
            story.append(img)
            story.append(Spacer(1, 0.2*inch))
        
        financial_data = [
            ["Component", "Annual Cost"],
            ["E-Commerce Platform", "$8,600"],
            ["Marketing Automation", "$9,000"],
            ["SEO & Content", "$20,000"],
            ["Process Automation", "$10,400"],
            ["Paid Advertising", "$36,000"],
            ["InnovLead Partnership", "$40,000"],
            ["<b>TOTAL INVESTMENT</b>", "<b>$124,000</b>"],
            ["<b>Less: CDAP Grant</b>", "<b>-$15,000</b>"],
            ["<b>Less: SR&ED Credits</b>", "<b>-$8,000 to -$15,000</b>"],
            ["<b>NET INVESTMENT</b>", "<b>$94,000 - $101,000</b>"]
        ]
        
        financial_table = Table(financial_data, colWidths=[3.5*inch, 2.5*inch])
        financial_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFD700')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('LINEABOVE', (0, 6), (-1, 6), 2, colors.black),
            ('LINEABOVE', (0, 9), (-1, 9), 2, colors.HexColor('#FFD700')),
            ('BACKGROUND', (0, 9), (-1, 9), colors.HexColor('#FFD700')),
            ('TEXTCOLOR', (0, 9), (-1, 9), colors.black),
            ('FONTNAME', (0, 9), (-1, 9), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 9), (-1, 9), 14),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8)
        ]))
        
        story.append(financial_table)
        
        story.append(PageBreak())
        
        # SLIDE 6: Year 1 Profitability
        story.append(Paragraph("Year 1 Profitability", heading_style))
        
        profit_data = [
            ["Metric", "Amount"],
            ["Revenue", "$439,650"],
            ["Gross Profit (65% margin)", "$285,772"],
            ["Operating Expenses", "$124,000"],
            ["<b>Net Profit</b>", "<b>$161,772</b>"],
            ["<b>Net Margin</b>", "<b>37%</b>"],
            ["<b>ROI</b>", "<b>160-188%</b>"]
        ]
        
        profit_table = Table(profit_data, colWidths=[3.5*inch, 2.5*inch])
        profit_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFD700')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 2, colors.black),
            ('BACKGROUND', (0, 3), (-1, -1), colors.HexColor('#00FF00')),
            ('TEXTCOLOR', (0, 3), (-1, -1), colors.black),
            ('FONTNAME', (0, 3), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 3), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10)
        ]))
        
        story.append(profit_table)
        
        story.append(Spacer(1, 0.3*inch))
        
        # 3-year trajectory
        trajectory_data = [
            ["Year", "Revenue", "Growth"],
            ["Year 1", "$440K", "—"],
            ["Year 2", "$850K", "93%"],
            ["Year 3", "$1.4M", "65%"],
            ["<b>Total 3-Year</b>", "<b>$2.69M</b>", "—"]
        ]
        
        trajectory_table = Table(trajectory_data, colWidths=[2*inch, 2*inch, 2*inch])
        trajectory_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00D4FF')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('LINEABOVE', (0, 4), (-1, 4), 2, colors.HexColor('#FFD700')),
            ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#FFD700')),
            ('TEXTCOLOR', (0, 4), (-1, 4), colors.black),
            ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8)
        ]))
        
        story.append(trajectory_table)
        
        story.append(PageBreak())
        
        # SLIDE 7: Why InnovLead
        story.append(Paragraph("Why InnovLead Canada?", heading_style))
        
        innovlead_text = """
        <b>Leadership: William Meléndez Salas, MBA</b><br/>
        CEO & Principal – InnovLead Canada Inc.<br/>
        <br/>
        <b>Credentials:</b><br/>
        ✅ ISO 27001 Lead Implementer<br/>
        ✅ PIPEDA, Loi 25, CASL Compliance Expert<br/>
        ✅ MBA in Big Data & Project Management<br/>
        ✅ 10× Colombian Judo Champion<br/>
        ✅ Quant Trader (18% CAGR algorithms)<br/>
        ✅ 6-time Published Author<br/>
        <br/>
        <b>Track Record:</b><br/>
        ✅ +30% YoY InnovLead growth<br/>
        ✅ 10 years AI-led digitalization<br/>
        ✅ ISO 27001 certified operations<br/>
        ✅ Enterprise security & compliance<br/>
        ✅ Growth marketing expertise<br/>
        <br/>
        <b>Why This Matters:</b><br/>
        → Not a vendor, a strategic partner<br/>
        → Compliance-first (no future liability)<br/>
        → Data-driven (quant algorithms optimize every dollar)<br/>
        → Hands-on (continuous optimization, not "set it and forget it")
        """
        
        story.append(Paragraph(innovlead_text, body_style))
        
        story.append(PageBreak())
        
        # SLIDE 8: Next Steps
        story.append(Paragraph("Next Steps", heading_style))
        
        next_steps_text = """
        <b>Immediate Actions:</b><br/>
        <br/>
        <b>1. Discovery Session (90 minutes)</b><br/>
        Deep-dive into business goals, technical requirements, timeline alignment<br/>
        <br/>
        <b>2. Funding Applications (1 week)</b><br/>
        CDAP grant submission ($15K), SR&ED documentation, BDC financing intro<br/>
        <br/>
        <b>3. Contract & Kickoff (Day 14-21)</b><br/>
        Partnership agreement, Phase 1 launch, team introductions<br/>
        <br/>
        <br/>
        <b>Timeline to Market:</b><br/>
        → Day 0: Proposal accepted<br/>
        → Day 21: Kickoff & Phase 1 begins<br/>
        → Day 90: Platform live, automation running<br/>
        → Day 180: First major campaign (Holiday 2025)<br/>
        <br/>
        <br/>
        <b>Contact Information:</b><br/>
        William Meléndez Salas, MBA<br/>
        CEO & Principal – InnovLead Canada Inc.<br/>
        📧 wms090807@gmail.com<br/>
        🔗 linkedin.com/in/william-m-salas<br/>
        📅 calendly.com/innovlead-ca
        """
        
        story.append(Paragraph(next_steps_text, body_style))
        
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(
            "<b>Let's build Canada's leading gold & silver jewelry e-commerce brand together.</b> 💎",
            highlight_style
        ))
        
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(
            '<i>"The consultancy is the moat. The automation is the product. The vault is the asset."</i>',
            ParagraphStyle('quote', parent=body_style, alignment=TA_CENTER, fontSize=10, textColor=colors.HexColor('#FFD700'))
        ))
        
        # Build PDF
        doc.build(story)
        
        print(f"\nPDF generated successfully!")
        print(f"Saved to: {pdf_filename}")
        
        return pdf_filename


def main():
    """Run illustrated PDF generation"""
    if len(sys.argv) < 2:
        print("Usage: python generate_illustrated_proposal_pdf.py '<Company Name>'")
        print("Example: python generate_illustrated_proposal_pdf.py 'El Dorado Gold and Silver'")
        sys.exit(1)
    
    company_name = sys.argv[1]
    
    generator = IllustratedProposalGenerator(company_name)
    pdf_path = generator.create_pdf()
    
    print("\n" + "="*60)
    print("Illustrated Proposal PDF Complete!")
    print("="*60)
    print(f"\nFile: {pdf_path}")
    print(f"Company: {company_name}")
    print(f"AI Illustrations: Integrated with KeiAI")
    print("\nReady to send to client!")


if __name__ == "__main__":
    main()
