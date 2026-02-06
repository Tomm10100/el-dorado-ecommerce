"""
Seed educational content into the database
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from database.connection import SessionLocal
from database.models import Module, Lesson, PIPEDATip

def seed_modules_and_lessons():
    db = SessionLocal()
    
    try:
        # Check if already seeded
        existing = db.query(Module).first()
        if existing:
            print("Content already exists. Skipping...")
            return
        
        print("Adding educational content...")
        
        # Module 1: AI Ethics
        module1 = Module(
            module_code="ai_ethics",
            title="AI Ethics & Responsible AI",
            description="Learn about ethical AI development, recognizing bias, and responsible use of generative AI tools.",
            order_index=1,
            total_lessons=5,
            estimated_duration_minutes=45,
            is_published=True
        )
        db.add(module1)
        db.flush()
        
        lessons_m1 = [
            Lesson(module_id=module1.id, title="AI Fundamentals", order_index=1, 
                   content="**Welcome to AI Education!**\n\nArtificial Intelligence is transforming our world. This lesson covers the basics of what AI is, how it works, and why it matters for everyone - not just tech experts.\n\n**Key Topics:**\n• What is AI?\n• Machine Learning basics\n• AI in everyday life\n• Why AI literacy matters\n\nUnderstanding AI empowers you to use it responsibly and recognize its impact on society."),
            
            Lesson(module_id=module1.id, title="Recognizing Bias in AI", order_index=2,
                   content="**Understanding AI Bias**\n\nAI systems can inherit human biases from training data. Learn to identify and address bias.\n\n**Common Types of Bias:**\n• Data bias\n• Algorithmic bias\n• Confirmation bias\n• Representation bias\n\n**Why It Matters:**\nBiased AI can lead to unfair outcomes in hiring, lending, healthcare, and criminal justice.\n\n**What You Can Do:**\n• Question AI decisions\n• Advocate for diverse datasets\n• Support ethical AI development"),
            
            Lesson(module_id=module1.id, title="Generative AI Ethics", order_index=3,
                   content="**Ethical Use of ChatGPT, Claude & Other AI**\n\nGenerative AI is powerful but comes with responsibilities.\n\n**Ethical Considerations:**\n• Copyright and intellectual property\n• Privacy and data security\n• Misinformation risks\n• Job displacement concerns\n• Environmental impact\n\n**Best Practices:**\n✓ Verify AI-generated information\n✓ Credit AI assistance when used\n✓ Protect sensitive data\n✓ Use AI to augment, not replace, human judgment\n✓ Consider the broader impact"),
            
            Lesson(module_id=module1.id, title="AI in Public Services", order_index=4,
                   content="**AI for Social Good**\n\nHow AI can benefit communities and nonprofits.\n\n**Applications:**\n• Healthcare diagnostics\n• Education personalization\n• Disaster response\n• Accessibility tools\n• Environmental monitoring\n\n**For NGOs:**\nAI can help with:\n• Donor management\n• Impact analysis\n• Resource optimization\n• Community outreach\n• Grant writing\n\n**Remember:** Technology should serve people, not the other way around."),
            
            Lesson(module_id=module1.id, title="Building Responsible AI", order_index=5,
                   content="**Principles of Responsible AI**\n\nHow to ensure AI development benefits everyone.\n\n**Core Principles:**\n1. **Fairness** - Equal treatment across groups\n2. **Transparency** - Explainable decisions\n3. **Privacy** - Data protection\n4. **Accountability** - Clear responsibility\n5. **Safety** - Minimize harm\n6. **Inclusivity** - Diverse perspectives\n\n**Your Role:**\nWhether you're a developer, user, or advocate, YOU can promote responsible AI through awareness, education, and action.\n\n**Next Steps:**\nApply these principles in your work and community.")
        ]
        
        for lesson in lessons_m1:
            db.add(lesson)
        
        # Module 2: PIPEDA Privacy
        module2 = Module(
            module_code="pipeda_privacy",
            title="Privacy in Canada (PIPEDA)",
            description="Understand your privacy rights under Canada's Personal Information Protection and Electronic Documents Act.",
            order_index=2,
            total_lessons=6,
            estimated_duration_minutes=60,
            is_published=True
        )
        db.add(module2)
        db.flush()
        
        lessons_m2 = [
            Lesson(module_id=module2.id, title="Introduction to PIPEDA", order_index=1,
                   content="**Canada's Privacy Law**\n\nPIPEDA governs how private sector organizations collect, use, and disclose personal information.\n\n**What is PIPEDA?**\nPersonal Information Protection and Electronic Documents Act - Canada's federal privacy law.\n\n**Who It Applies To:**\n• Private sector organizations\n• Federal works, undertakings, and businesses\n• Organizations with interprovincial/international data flows\n\n**10 Fair Information Principles:**\n1. Accountability\n2. Identifying Purposes\n3. Consent\n4. Limiting Collection\n5. Limiting Use, Disclosure, Retention\n6. Accuracy\n7. Safeguards\n8. Openness\n9. Individual Access\n10. Challenging Compliance"),
            
            Lesson(module_id=module2.id, title="Your Privacy Rights", order_index=2,
                   content="**What Rights Do You Have?**\n\nUnder PIPEDA, you have strong privacy protections.\n\n**Your Rights:**\n✓ **Right to Know** - What info is collected and why\n✓ **Right to Access** - Request your personal data\n✓ **Right to Correction** - Fix inaccurate information\n✓ **Right to Withdraw Consent** - Change your mind\n✓ **Right to Complain** - File complaints with Privacy Commissioner\n\n**How to Exercise Rights:**\n1. Contact the organization's privacy officer\n2. Make written requests\n3. Provide necessary identification\n4. Follow up within reasonable time\n\n**Contact:**\nPrivacy Commissioner of Canada\n📞 1-800-282-1376"),
            
            Lesson(module_id=module2.id, title="Consent and Data Collection", order_index=3,
                   content="**Understanding Consent**\n\nMeaningful consent is the foundation of privacy protection.\n\n**Valid Consent Must Be:**\n• **Informed** - You understand what you're agreeing to\n• **Voluntary** - No coercion or pressure\n• **Specific** - Clear about what's being collected\n• **Time-limited** - Can be withdrawn\n\n**Types of Consent:**\n• Express (explicit agreement)\n• Implied (from actions)\n• Opt-in vs Opt-out\n\n**Red Flags:**\n⚠️ Hidden consent in long terms\n⚠️ All-or-nothing access\n⚠️ Pre-checked boxes\n⚠️ Unclear language\n\n**Tip:** Read privacy policies before agreeing!"),
            
            Lesson(module_id=module2.id, title="Data Breach Response", order_index=4,
                   content="**What To Do If Your Data Is Breached**\n\nData breaches happen. Know your rights and responses.\n\n**Organization Obligations:**\nMust notify you if breach poses \"real risk of significant harm\"\n\n**Your Immediate Actions:**\n1. ✓ Change passwords immediately\n2. ✓ Enable 2-factor authentication\n3. ✓ Monitor accounts for suspicious activity\n4. ✓ Place fraud alerts with credit bureaus\n5. ✓ Document everything\n\n**Report To:**\n• Privacy Commissioner\n• Police (if identity theft)\n• Credit bureaus\n• Financial institutions\n\n**Prevention:**\n• Use unique passwords\n• Limit data sharing\n• Regular security updates"),
            
            Lesson(module_id=module2.id, title="Privacy for NGOs", order_index=5,
                   content="**PIPEDA Compliance for Nonprofits**\n\nNonprofits must also protect personal information.\n\n**What NGOs Collect:**\n• Donor information\n• Volunteer data\n• Beneficiary records\n• Employee information\n• Event registrations\n\n**Compliance Steps:**\n1. Appoint privacy officer\n2. Create privacy policy\n3. Obtain proper consent\n4. Secure data storage\n5. Train staff\n6. Plan for breaches\n7. Allow data access requests\n\n**Low-Cost Tools:**\n• Encrypted email (ProtonMail)\n• Secure forms (JotForm)\n• Password managers\n• Cloud storage with encryption\n\n**Remember:** Privacy builds trust with donors and beneficiaries."),
            
            Lesson(module_id=module2.id, title="Exercising Your Rights", order_index=6,
                   content="**Take Control of Your Privacy**\n\nPractical steps to protect your data.\n\n**Action Plan:**\n\n**Week 1: Audit**\n• List organizations with your data\n• Review privacy settings\n• Check what's public online\n\n**Week 2: Request**\n• Request your data from major platforms\n• Verify accuracy\n• Request corrections if needed\n\n**Week 3: Protect**\n• Update passwords\n• Enable 2FA everywhere\n• Delete unused accounts\n\n**Week 4: Maintain**\n• Set calendar reminders for reviews\n• Stay informed about breaches\n• Exercise rights regularly\n\n**Resources:**\n• priv.gc.ca\n• Get Cyber Safe program\n• Your provincial privacy commissioner")
        ]
        
        for lesson in lessons_m2:
            db.add(lesson)
        
        # Module 3: Social Automation
        module3 = Module(
            module_code="social_automation",
            title="Social Automation Tools",
            description="Learn low-code automation platforms like n8n to boost productivity without expensive software.",
            order_index=3,
            total_lessons=4,
            estimated_duration_minutes=50,
            is_published=True
        )
        db.add(module3)
        db.flush()
        
        lessons_m3 = [
            Lesson(module_id=module3.id, title="Automation Basics", order_index=1,
                   content="**Work Smarter, Not Harder**\n\nAutomation can save hours of repetitive work.\n\n**What is Automation?**\nUsing software to perform tasks automatically without manual intervention.\n\n**Common Use Cases:**\n• Email management\n• Social media posting\n• Data entry\n• File organization\n• Report generation\n• Customer responses\n\n**Benefits for NGOs:**\n• Save time and money\n• Reduce errors\n• Scale operations\n• Focus on mission\n• Improve consistency\n\n**Getting Started:**\nStart small with one repetitive task."),
            
            Lesson(module_id=module3.id, title="Introduction to n8n", order_index=2,
                   content="**Free Open-Source Automation**\n\nn8n is a powerful, free alternative to expensive automation tools.\n\n**What is n8n?**\nA workflow automation tool you can self-host for free.\n\n**vs Zapier:**\n• n8n: Free, open-source, unlimited workflows\n• Zapier: $20-$100+/month, limited workflows\n\n**Key Features:**\n✓ 300+ integrations\n✓ Visual workflow builder\n✓ No coding required\n✓ Self-hosted (data privacy)\n✓ Unlimited workflows\n\n**Popular Workflows:**\n• Email → Spreadsheet\n• Form → Slack notification\n• Social media scheduler\n• Donor thank-you automation\n\n**Get Started:**\nn8n.io"),
            
            Lesson(module_id=module3.id, title="Workflow Design", order_index=3,
                   content="**Building Effective Workflows**\n\nHow to design automation that actually works.\n\n**Design Process:**\n\n**1. Identify Task**\n• What's repetitive?\n• What's time-consuming?\n• What's error-prone?\n\n**2. Map Steps**\n• List every manual step\n• Note decision points\n• Identify data sources\n\n**3. Build Workflow**\n• Start simple\n• Test frequently\n• Add complexity gradually\n\n**4. Monitor & Improve**\n• Track success rate\n• Gather feedback\n• Refine as needed\n\n**Best Practices:**\n• Document workflows\n• Add error handling\n• Test with real data\n• Have backup plans"),
            
            Lesson(module_id=module3.id, title="Maximum Impact, Zero Budget", order_index=4,
                   content="**Free Tools for NGOs**\n\nPowerful automation without breaking the bank.\n\n**Essential Free Tools:**\n\n**Automation:**\n• n8n (workflows)\n• IFTTT (simple triggers)\n• Integromat (Make.com free tier)\n\n**Communication:**\n• Telegram bots\n• Discord webhooks\n• Slack (free plan)\n\n**Data:**\n• Google Sheets (spreadsheets)\n• Airtable (databases)\n• Notion (knowledge base)\n\n**Storage:**\n• Google Drive (15GB)\n• Dropbox (2GB)\n• OneDrive (5GB)\n\n**Sample Workflow:**\nDonation form → Email thank you → Add to spreadsheet → Slack notification → Monthly report\n\nAll free, all automated!\n\n**Next Steps:**\nStart with ONE workflow this week.")
        ]
        
        for lesson in lessons_m3:
            db.add(lesson)
        
        # Add PIPEDA Tips
        tips = [
            PIPEDATip(title="What is Consent?", category="consent", target_audience="general",
                     content="Organizations must get your consent before collecting, using, or sharing your personal information. You have the right to say no or withdraw consent anytime."),
            
            PIPEDATip(title="Read Before You Click", category="consent", target_audience="general",
                     content="Always read privacy policies before agreeing. Look for: what data is collected, how it's used, who it's shared with, and how long it's kept."),
            
            PIPEDATip(title="You Can Say No", category="individual_rights", target_audience="general",
                     content="You don't have to give consent just because it's asked. Organizations must respect your refusal unless they have legal grounds to collect without consent."),
            
            PIPEDATip(title="Access Your Data", category="individual_rights", target_audience="general",
                     content="You have the right to access your personal information held by organizations. Request it in writing and they must respond within 30 days."),
            
            PIPEDATip(title="Fix Incorrect Information", category="individual_rights", target_audience="general",
                     content="If your personal information is inaccurate, you can request corrections. Organizations must either fix it or note your correction request in your file."),
            
            PIPEDATip(title="What is a Data Breach?", category="data_breach", target_audience="general",
                     content="A data breach is unauthorized access to personal information. Organizations must notify you if there's a real risk of significant harm."),
            
            PIPEDATip(title="After a Breach", category="data_breach", target_audience="general",
                     content="If notified of a breach: change passwords immediately, enable 2FA, monitor accounts, and consider credit monitoring. Report suspicious activity right away."),
            
            PIPEDATip(title="File a Complaint", category="individual_rights", target_audience="general",
                     content="If an organization violates your privacy rights, file a complaint with the Privacy Commissioner of Canada at 1-800-282-1376 or www.priv.gc.ca")
        ]
        
        for tip in tips:
            db.add(tip)
        
        db.commit()
        print("[OK] Added 3 modules")
        print("[OK] Added 15 lessons")
        print("[OK] Added 8 PIPEDA tips")
        print("\n[SUCCESS] All content loaded!")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    seed_modules_and_lessons()
