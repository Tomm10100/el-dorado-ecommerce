"""
Seed initial data into the database
Populates modules, lessons, and PIPEDA tips
"""
import json
from sqlalchemy.orm import Session
from database.models import Module, Lesson, PIPEDATip


def seed_initial_data(db: Session):
    """Seed modules, lessons, and PIPEDA tips"""
    
    # Check if data already exists
    existing_modules = db.query(Module).count()
    if existing_modules > 0:
        print("⚠️  Database already contains data. Skipping seed.")
        return
    
    # Seed Modules
    seed_modules(db)
    
    # Seed Lessons
    seed_lessons(db)
    
    # Seed PIPEDA Tips
    seed_pipeda_tips(db)
    
    db.commit()
    print("✅ Seeded modules, lessons, and PIPEDA tips")


def seed_modules(db: Session):
    """Seed educational modules"""
    modules_data = [
        {
            "module_code": "ai_ethics",
            "title": "AI Ethics & Responsible AI",
            "description": "Learn the fundamentals of ethical AI, bias recognition, and responsible use of generative AI tools.",
            "order_index": 1,
            "total_lessons": 5,
            "estimated_duration_minutes": 45,
            "is_published": True
        },
        {
            "module_code": "privacy_canada",
            "title": "Privacy in Canada (PIPEDA)",
            "description": "Understand your privacy rights under PIPEDA, data protection, and compliance for individuals and NGOs.",
            "order_index": 2,
            "total_lessons": 6,
            "estimated_duration_minutes": 60,
            "is_published": True
        },
        {
            "module_code": "social_automation",
            "title": "Social Automation with Low-Code Tools",
            "description": "Master automation basics and low-code platforms like n8n to boost productivity without budget constraints.",
            "order_index": 3,
            "total_lessons": 4,
            "estimated_duration_minutes": 40,
            "is_published": True
        }
    ]
    
    for module_data in modules_data:
        module = Module(**module_data)
        db.add(module)


def seed_lessons(db: Session):
    """Seed lessons for each module"""
    
    # Module 1: AI Ethics & Responsible AI
    ai_ethics_lessons = [
        {
            "lesson_code": "ai_fundamentals",
            "title": "Understanding AI Fundamentals",
            "content": """Welcome to AI Ethics! 🤖

**What is Artificial Intelligence?**
AI refers to computer systems that can perform tasks typically requiring human intelligence: learning, problem-solving, pattern recognition, and decision-making.

**Types of AI:**
- **Narrow AI**: Specialized systems (e.g., voice assistants, recommendation engines)
- **General AI**: Human-level intelligence across all domains (theoretical)
- **Generative AI**: Creates new content (text, images, code) based on patterns

**Key Concepts:**
- Machine Learning: Systems that improve through experience
- Deep Learning: Neural networks inspired by the brain
- Natural Language Processing: Understanding human language

**Why Ethics Matter:**
AI systems can amplify biases, make unfair decisions, and impact vulnerable communities disproportionately.

🎯 **Your Role:** As an informed citizen, you can advocate for ethical AI that serves everyone.""",
            "order_index": 1,
            "has_quiz": False
        },
        {
            "lesson_code": "recognizing_bias",
            "title": "Recognizing AI Bias",
            "content": """🔍 Understanding AI Bias

**What is AI Bias?**
AI systems learn from data. If that data reflects historical discrimination or incomplete representation, the AI will perpetuate those biases.

**Real-World Examples:**
- Facial recognition less accurate for people of color
- Hiring algorithms favoring male candidates
- Credit scoring discriminating against marginalized groups

**Types of Bias:**
1. **Data Bias**: Training data doesn't represent reality
2. **Algorithmic Bias**: The model's design favors certain outcomes
3. **Deployment Bias**: How the system is used in practice

**How to Identify Bias:**
- Question: Who created this dataset?
- Ask: Are all groups fairly represented?
- Verify: Are outcomes equitable across demographics?

**Your Power:**
Demand transparency, diversity in AI teams, and accountability from organizations using AI systems.

🌍 **Remember:** Biased AI isn't inevitable—it's a choice we can change.""",
            "order_index": 2,
            "has_quiz": False
        },
        {
            "lesson_code": "generative_ai_ethics",
            "title": "Ethical Use of Generative AI",
            "content": """✨ Responsible Generative AI Use

**What is Generative AI?**
Systems like ChatGPT, Claude, DALL-E that create new content based on learned patterns.

**Ethical Principles:**

1. **Transparency**: Disclose when content is AI-generated
2. **Attribution**: Don't claim AI output as entirely your own work
3. **Verification**: Always fact-check AI-generated information
4. **Privacy**: Never input sensitive personal data
5. **Fairness**: Be aware AI can perpetuate stereotypes

**Best Practices:**
✅ Use AI as a tool to augment, not replace, human creativity
✅ Review and edit AI outputs critically
✅ Understand the limitations (hallucinations, outdated info)
✅ Respect intellectual property and copyright
✅ Consider environmental impact (energy consumption)

**Red Flags:**
❌ Using AI to deceive or manipulate
❌ Generating deepfakes without consent
❌ Automating decisions affecting people's lives without oversight
❌ Replacing human judgment in sensitive contexts

🎓 **InnovLead's Stance:** AI should empower, not exploit.""",
            "order_index": 3,
            "has_quiz": False
        },
        {
            "lesson_code": "ai_public_services",
            "title": "AI in Public Services",
            "content": """🏛️ AI in Government & Public Services

**Current Applications:**
- Social benefit eligibility screening
- Predictive policing
- Healthcare resource allocation
- Educational assessments

**Promises:**
- Increased efficiency
- Reduced human error
- Data-driven insights
- Cost savings

**Risks:**
- Lack of transparency ("black box" decisions)
- Bias against vulnerable populations
- Reduced human discretion and empathy
- Privacy violations

**Your Rights in Canada:**
Under Canadian law, you have the right to:
✓ Know when AI is being used to make decisions about you
✓ Understand the logic behind automated decisions
✓ Challenge decisions and request human review
✓ Access your personal data

**Advocacy Actions:**
1. Demand algorithmic impact assessments
2. Push for community oversight boards
3. Support regulations requiring explainable AI
4. Hold institutions accountable for discriminatory outcomes

🗣️ **Speak Up:** Public services should serve the public, not algorithms.""",
            "order_index": 4,
            "has_quiz": False
        },
        {
            "lesson_code": "building_responsible_ai",
            "title": "Building Responsible AI Systems",
            "content": """🔨 Principles of Responsible AI Development

**Core Principles:**

1. **Fairness**: Equal treatment across all groups
2. **Accountability**: Clear responsibility for outcomes
3. **Transparency**: Explainable decision-making processes
4. **Privacy**: Strong data protection safeguards
5. **Safety**: Rigorous testing and monitoring

**The InnovLead Framework:**

**Design Phase:**
- Diverse, multidisciplinary teams
- Community stakeholder input
- Bias audits on training data
- Clear ethical guidelines

**Development Phase:**
- Regular fairness testing
- Documentation of decisions
- Privacy-by-design architecture
- Security audits

**Deployment Phase:**
- Ongoing monitoring for bias drift
- Human oversight mechanisms
- Feedback loops with affected communities
- Transparent reporting

**For NGOs & Community Organizations:**
Even without technical expertise, you can:
✓ Ask vendors about bias testing
✓ Demand diverse training data
✓ Require human appeal processes
✓ Insist on regular audits

🌟 **Your Voice Matters:** Ethical AI requires community participation, not just technical solutions.

**Congratulations!** You've completed Module 1: AI Ethics & Responsible AI.""",
            "order_index": 5,
            "has_quiz": False
        }
    ]
    
    # Module 2: Privacy in Canada (PIPEDA)
    privacy_lessons = [
        {
            "lesson_code": "intro_pipeda",
            "title": "Introduction to PIPEDA",
            "content": """🔒 Welcome to Privacy in Canada

**What is PIPEDA?**
The Personal Information Protection and Electronic Documents Act (PIPEDA) is Canada's federal privacy law governing how private sector organizations collect, use, and disclose personal information.

**Who Does PIPEDA Apply To?**
- Private sector organizations
- Federal works, undertakings, and businesses
- Organizations operating across provincial borders

**What is Personal Information?**
Any information about an identifiable individual:
- Name, address, phone number
- Email, IP address
- Financial information
- Health records
- Biometric data
- Online identifiers

**The 10 Fair Information Principles:**
1. Accountability
2. Identifying Purposes
3. Consent
4. Limiting Collection
5. Limiting Use, Disclosure, and Retention
6. Accuracy
7. Safeguards
8. Openness
9. Individual Access
10. Challenging Compliance

**Why This Matters:**
Your personal data has value. PIPEDA gives you control over how organizations use it.

🛡️ **Know Your Rights:** Privacy is a fundamental right, not a privilege.""",
            "lesson_code": "intro_pipeda",
            "order_index": 1,
            "has_quiz": False
        },
        {
            "lesson_code": "data_protection_rights",
            "title": "Your Data Protection Rights",
            "content": """📋 What Rights Do You Have Under PIPEDA?

**1. Right to Know**
Organizations must tell you:
- What information they collect
- Why they need it
- How they'll use it
- Who they'll share it with

**2. Right to Consent**
You must give meaningful consent before your information is collected, used, or disclosed.

**Types of Consent:**
- **Express Consent**: Clear, explicit agreement (required for sensitive data)
- **Implied Consent**: Inferred from your actions (for non-sensitive data)

**3. Right to Access**
You can request:
- What personal information an organization holds about you
- How it's been used
- Who it's been disclosed to

**4. Right to Correction**
You can challenge the accuracy and completeness of your information and request corrections.

**5. Right to Withdraw Consent**
You can withdraw consent at any time (with some legal exceptions).

**How to Exercise Your Rights:**
1. Submit a written request
2. Organization must respond within 30 days
3. Access to information should be free or low-cost
4. If denied, you can file a complaint with the Privacy Commissioner

⚖️ **Remember:** Organizations must balance your rights with legitimate business needs.""",
            "lesson_code": "data_protection_rights",
            "order_index": 2,
            "has_quiz": False
        },
        {
            "lesson_code": "consent_management",
            "title": "Understanding Consent",
            "content": """✍️ The Foundation of Privacy: Consent

**What Makes Consent Valid?**

Consent must be:
- **Informed**: You understand what you're agreeing to
- **Voluntary**: No coercion or pressure
- **Specific**: Clear about what data and purposes
- **Current**: Not expired or outdated

**Red Flags - Invalid Consent:**
❌ Buried in long terms of service
❌ "Take it or leave it" for unrelated services
❌ Pre-checked boxes
❌ Unclear or ambiguous language
❌ No option to refuse

**Best Practices for Organizations:**
✅ Use plain language
✅ Separate consent requests by purpose
✅ Offer granular choices
✅ Make it easy to withdraw consent
✅ Document all consent interactions

**For Individuals:**
🔍 **Before You Consent:**
- Read privacy policies (even briefly!)
- Understand what you're sharing
- Ask: Is this necessary?
- Check if you can opt out later

**For NGOs:**
Your organization must:
- Obtain proper consent from donors, volunteers, beneficiaries
- Document consent clearly
- Respect withdrawal requests promptly
- Train staff on consent requirements

💡 **Pro Tip:** When in doubt, ask for express consent—it's always safer.""",
            "lesson_code": "consent_management",
            "order_index": 3,
            "has_quiz": False
        },
        {
            "lesson_code": "data_breach_response",
            "title": "Data Breaches & Your Rights",
            "content": """🚨 Data Breaches: What You Need to Know

**What is a Data Breach?**
Unauthorized access, collection, use, disclosure, disposal, or loss of personal information.

**Examples:**
- Hacking or cyberattacks
- Lost or stolen devices
- Accidental disclosure
- Insider threats
- Ransomware

**Mandatory Breach Reporting (Since 2018):**

Organizations MUST:
1. **Report to Privacy Commissioner** if breach poses "real risk of significant harm"
2. **Notify affected individuals** about the breach
3. **Keep records** of all breaches

**What Should Notification Include?**
- Nature of the breach
- Date or time period
- Type of information involved
- Steps the organization is taking
- Steps you can take to reduce harm
- Contact information for inquiries

**Your Actions After a Breach:**

**Immediate:**
✓ Change passwords (use unique, strong passwords)
✓ Enable two-factor authentication
✓ Monitor financial accounts

**Short-term:**
✓ Place fraud alerts with credit bureaus
✓ Review credit reports
✓ Watch for phishing attempts

**Long-term:**
✓ Consider credit monitoring services
✓ File complaint with Privacy Commissioner if organization didn't handle it properly
✓ Seek legal advice if you suffered harm

🛡️ **Prevention:** Use password managers, enable 2FA everywhere, minimize data sharing.""",
            "lesson_code": "data_breach_response",
            "order_index": 4,
            "has_quiz": False
        },
        {
            "lesson_code": "privacy_for_ngos",
            "title": "Privacy for NGOs",
            "content": """🤝 Privacy Compliance for Nonprofits & NGOs

**Why Privacy Matters for NGOs:**
- Build trust with donors and beneficiaries
- Protect vulnerable populations
- Comply with legal obligations
- Prevent reputational damage

**Common Privacy Challenges:**

1. **Donor Data:**
   - Credit card information
   - Contact details
   - Donation history

2. **Beneficiary Data:**
   - Often sensitive (health, financial hardship)
   - Vulnerability requires extra care

3. **Volunteer Information:**
   - Background checks
   - Personal references
   - Sensitive information

**PIPEDA Compliance Checklist:**

✅ **Accountability:**
- Designate a privacy officer
- Create privacy policy
- Train staff and volunteers

✅ **Consent:**
- Get clear consent for data collection
- Explain how data will be used
- Offer opt-outs for communications

✅ **Data Minimization:**
- Collect only what you need
- Delete data when no longer needed
- Review retention schedules

✅ **Security:**
- Use encryption
- Secure physical files
- Control access to sensitive data
- Regular security audits

✅ **Transparency:**
- Publish privacy policy
- Make it easy to find
- Update regularly

**Practical Tips:**
💡 Use secure, PIPEDA-compliant CRM tools
💡 Get legal review of data practices
💡 Consider cyber insurance
💡 Have incident response plan ready

🌟 **InnovLead Can Help:** Free resources and templates at innovlead.org/privacy""",
            "lesson_code": "privacy_for_ngos",
            "order_index": 5,
            "has_quiz": False
        },
        {
            "lesson_code": "individual_rights_pipeda",
            "title": "Exercising Your PIPEDA Rights",
            "content": """⚖️ How to Exercise Your Privacy Rights

**Filing an Access Request:**

**Step 1: Identify the Organization**
Find their privacy officer or contact information (check privacy policy).

**Step 2: Submit Written Request**
Include:
- Your full name
- Contact information
- Specific information you're requesting
- Any relevant dates or details
- Proof of identity

**Step 3: Wait for Response**
- Organization has 30 days to respond
- Can extend by 30 days with explanation
- Must provide information free or for minimal cost

**If Your Request Is Denied:**
- Request written explanation
- File complaint with Privacy Commissioner
- Seek legal advice

**Filing a Privacy Complaint:**

**When to Complain:**
- Organization violated PIPEDA
- Didn't respond to access request
- Refused correction request
- Handled breach poorly

**How to File:**
1. Try to resolve with organization first
2. Gather documentation
3. File complaint with Office of the Privacy Commissioner of Canada
4. Can file online at priv.gc.ca

**What Happens Next:**
- Commissioner investigates
- May mediate resolution
- Issues findings
- Can take organization to Federal Court

**Resources:**

📞 **Privacy Commissioner of Canada:**
- Phone: 1-800-282-1376
- Web: www.priv.gc.ca
- Email: info@priv.gc.ca

🎓 **InnovLead Support:**
- Free consultation: education@innovlead.org
- Community forums: @InnovLeadCommunity
- Privacy toolkit: innovlead.org/pipeda

**Congratulations!** You've completed Module 2: Privacy in Canada (PIPEDA).

🏆 **You're now equipped to protect your privacy and advocate for others!**""",
            "lesson_code": "individual_rights_pipeda",
            "order_index": 6,
            "has_quiz": False
        }
    ]
    
    # Module 3: Social Automation
    automation_lessons = [
        {
            "lesson_code": "automation_basics",
            "title": "Automation Basics for Social Good",
            "content": """⚡ Introduction to Automation

**What is Automation?**
Using technology to perform repetitive tasks without human intervention, freeing you to focus on meaningful work.

**Why Automation for NGOs?**
- **Save Time**: Automate admin tasks
- **Reduce Errors**: Consistency in processes
- **Scale Impact**: Do more with limited resources
- **Focus on Mission**: Spend time on what matters

**Common Automation Use Cases:**

**1. Communication:**
- Welcome emails for new donors
- Thank you messages
- Event reminders
- Newsletter scheduling

**2. Data Management:**
- Form submissions to spreadsheets
- CRM updates
- Report generation
- Database backups

**3. Social Media:**
- Post scheduling
- Cross-platform sharing
- Engagement tracking
- Content curation

**4. Operations:**
- Invoice processing
- Expense tracking
- Volunteer scheduling
- Inventory management

**Automation Principles:**

✅ **Start Small**: One process at a time
✅ **Document First**: Map out current workflow
✅ **Test Thoroughly**: Ensure accuracy before going live
✅ **Monitor**: Check automation regularly
✅ **Stay Human**: Keep human oversight for critical decisions

**The Low-Code Revolution:**
You don't need to be a programmer! Modern tools use visual interfaces and pre-built components.

🚀 **Next:** We'll explore n8n, a powerful free automation platform.""",
            "lesson_code": "automation_basics",
            "order_index": 1,
            "has_quiz": False
        },
        {
            "lesson_code": "intro_n8n",
            "title": "Introduction to n8n",
            "content": """🔧 n8n: Your Automation Powerhouse

**What is n8n?**
A free, open-source workflow automation tool that connects different apps and services without coding.

**Why n8n for NGOs?**
✅ **Free & Open Source**: No licensing costs
✅ **Self-Hosted**: Keep data under your control
✅ **Visual Editor**: Drag-and-drop interface
✅ **400+ Integrations**: Gmail, Google Sheets, Slack, Airtable, etc.
✅ **Privacy-Friendly**: Perfect for PIPEDA compliance

**Key Concepts:**

**1. Workflows:**
A series of connected steps (nodes) that automate a process

**2. Nodes:**
Building blocks representing actions or triggers
- **Trigger Nodes**: Start the workflow (e.g., "New email received")
- **Action Nodes**: Perform tasks (e.g., "Add row to spreadsheet")
- **Logic Nodes**: Add conditions and decisions

**3. Connections:**
Lines showing how data flows between nodes

**Example Workflow:**
```
New Form Submission (Trigger)
    ↓
Extract Data (Transform)
    ↓
Add to Google Sheet (Action)
    ↓
Send Thank You Email (Action)
```

**Getting Started:**

**Cloud Version:**
- Visit n8n.cloud
- Free tier available
- Quick setup

**Self-Hosted (More Control):**
- Host on your own server
- Complete data privacy
- Unlimited workflows

**InnovLead Recommendation:**
Start with cloud for learning, move to self-hosted for production with sensitive data.

**Resources:**
📚 n8n Documentation: docs.n8n.io
🎓 InnovLead n8n Course: innovlead.org/n8n
💬 Community: community.n8n.io

🎯 **Next Lesson:** Building your first workflow!""",
            "lesson_code": "intro_n8n",
            "order_index": 2,
            "has_quiz": False
        },
        {
            "lesson_code": "workflow_design",
            "title": "Designing Effective Workflows",
            "content": """🎨 Workflow Design Best Practices

**The Workflow Design Process:**

**Step 1: Identify the Problem**
- What task is repetitive?
- How much time does it take?
- What's the error rate?
- How often does it happen?

**Step 2: Map Current Process**
Document every step, even small ones:
1. Trigger: What starts the process?
2. Steps: What happens in what order?
3. Decisions: Are there conditional paths?
4. Outcome: What's the desired result?

**Step 3: Design Automation**
- What can be automated?
- What needs human review?
- What are the edge cases?
- Where could it fail?

**Step 4: Build & Test**
- Start with a simple version
- Test with sample data
- Handle errors gracefully
- Add logging for troubleshooting

**Step 5: Deploy & Monitor**
- Roll out gradually
- Monitor for issues
- Gather feedback
- Iterate and improve

**Design Principles:**

**1. Keep It Simple**
- Start with basic workflows
- Add complexity only when needed
- One workflow, one purpose

**2. Error Handling**
- Plan for failures
- Add notifications for errors
- Include fallback options
- Log everything

**3. Documentation**
- Name workflows clearly
- Add notes to complex nodes
- Document assumptions
- Track changes

**4. Privacy by Design**
- Minimize data collection
- Encrypt sensitive data
- Control access carefully
- Delete data when done

**Real-World Example: Donor Thank You Automation**

**Problem**: Manual thank you emails take 2 hours/week

**Workflow:**
1. **Trigger**: New donation in payment system
2. **Get Donor Data**: Fetch name, email, amount
3. **Condition**: Check if amount > $100 (personalized response)
4. **Send Email**: Thank you template with donation details
5. **Update CRM**: Mark as "thanked"
6. **Log**: Record in donation tracker

**Time Saved**: 1.5 hours/week = 78 hours/year!

💡 **Pro Tip:** Automate the boring stuff, personalize the important stuff.""",
            "lesson_code": "workflow_design",
            "order_index": 3,
            "has_quiz": False
        },
        {
            "lesson_code": "productivity_no_budget",
            "title": "Maximum Productivity, Zero Budget",
            "content": """💪 Free Tools for Maximum Impact

**The NGO Tech Stack (100% Free):**

**1. Communication & Collaboration**
- **Slack** (Free tier): Team communication
- **Google Workspace for Nonprofits**: Email, docs, drive
- **Zoom** (Free tier): Video calls
- **Telegram**: Secure messaging

**2. Project Management**
- **Trello** (Free): Visual task boards
- **Asana** (Free for nonprofits): Project tracking
- **Notion** (Free): All-in-one workspace

**3. CRM & Fundraising**
- **Bitrix24** (Free tier): CRM and communication
- **HubSpot** (Free tier): Contact management
- **Mailchimp** (Free tier): Email marketing

**4. Design & Content**
- **Canva** (Free for nonprofits): Graphic design
- **GIMP**: Image editing
- **DaVinci Resolve**: Video editing

**5. Automation**
- **n8n**: Workflow automation
- **Zapier** (Free tier): App connections
- **IFTTT** (Free): Simple automations

**6. Data & Analytics**
- **Google Analytics**: Website tracking
- **Google Data Studio**: Dashboards
- **Airtable** (Free tier): Flexible databases

**Automation Ideas (No Budget Required):**

**Daily Operations:**
✓ Auto-save form submissions to Google Sheets
✓ Slack notifications for new donations
✓ Automated social media posting
✓ Email digest of weekly activities

**Donor Management:**
✓ Welcome sequence for new donors
✓ Birthday greetings
✓ Donation receipts
✓ Year-end tax summaries

**Volunteer Coordination:**
✓ Shift reminders
✓ Sign-up confirmations
✓ Training materials delivery
✓ Hour tracking

**Reporting:**
✓ Weekly metrics dashboards
✓ Monthly board reports
✓ Grant requirement tracking
✓ Impact measurement

**Getting Nonprofit Discounts:**

Many tech companies offer free or discounted services for registered nonprofits:

📋 **What You'll Need:**
- Registered charity number
- Organization domain email
- Mission statement
- Proof of nonprofit status

🔗 **Resources:**
- TechSoup: techsoup.org
- Google for Nonprofits: google.com/nonprofits
- Microsoft Nonprofits: microsoft.com/nonprofits

**InnovLead's Promise:**
🌟 We'll always prioritize free, open-source, privacy-respecting tools.

**Congratulations!** You've completed Module 3: Social Automation with Low-Code Tools.

🏆 **You now have the skills to transform your organization's efficiency—for free!**

---

**🎓 Certificate of Completion**
You've finished all three modules of the InnovLead Universal AI Education program. Your learning represents valuable skills that empower communities and advance digital equity.

**What's Next?**
- Join our community: @InnovLeadCommunity
- Access advanced resources: innovlead.org
- Share your knowledge with others
- Use /progreso to see your achievements

**Thank you for learning with InnovLead Foundation!**
Built with ❤️ for the people, by the people.""",
            "lesson_code": "productivity_no_budget",
            "order_index": 4,
            "has_quiz": False
        }
    ]
    
    # Add all lessons to database
    modules = db.query(Module).all()
    
    for module in modules:
        if module.module_code == "ai_ethics":
            for lesson_data in ai_ethics_lessons:
                lesson = Lesson(module_id=module.id, **lesson_data)
                db.add(lesson)
        elif module.module_code == "privacy_canada":
            for lesson_data in privacy_lessons:
                lesson = Lesson(module_id=module.id, **lesson_data)
                db.add(lesson)
        elif module.module_code == "social_automation":
            for lesson_data in automation_lessons:
                lesson = Lesson(module_id=module.id, **lesson_data)
                db.add(lesson)


def seed_pipeda_tips(db: Session):
    """Seed PIPEDA quick reference tips"""
    tips = [
        {
            "tip_code": "consent_basics",
            "category": "consent",
            "title": "What Makes Consent Valid?",
            "content": "Valid consent must be informed, voluntary, specific, and current. Organizations can't hide consent in long legal documents or use pre-checked boxes.",
            "target_audience": "citizens",
            "language": "en"
        },
        {
            "tip_code": "access_request",
            "category": "individual_rights",
            "title": "How to Request Your Data",
            "content": "You can request what personal information an organization holds about you. Submit a written request with proof of ID. They must respond within 30 days, usually for free.",
            "target_audience": "citizens",
            "language": "en"
        },
        {
            "tip_code": "data_breach_rights",
            "category": "data_breach",
            "title": "Your Rights During a Breach",
            "content": "If a data breach poses real risk of significant harm, organizations MUST notify you and the Privacy Commissioner. You should change passwords, monitor accounts, and can file a complaint if mishandled.",
            "target_audience": "citizens",
            "language": "en"
        },
        {
            "tip_code": "ngo_accountability",
            "category": "consent",
            "title": "NGO Accountability Requirements",
            "content": "NGOs must designate a privacy officer, create a privacy policy, obtain proper consent for data collection, and train staff on privacy obligations.",
            "target_audience": "NGOs",
            "language": "en"
        },
        {
            "tip_code": "data_minimization",
            "category": "consent",
            "title": "Collect Only What You Need",
            "content": "Organizations should collect only the minimum personal information necessary for the identified purpose. Ask yourself: Do we really need this data?",
            "target_audience": "NGOs",
            "language": "en"
        },
        {
            "tip_code": "withdraw_consent",
            "category": "individual_rights",
            "title": "You Can Withdraw Consent",
            "content": "You can withdraw consent for data use at any time (subject to legal restrictions). Organizations must make it easy to opt out and respect your decision promptly.",
            "target_audience": "citizens",
            "language": "en"
        },
        {
            "tip_code": "privacy_policy_checklist",
            "category": "consent",
            "title": "Privacy Policy Essentials",
            "content": "Your privacy policy should explain: what data you collect, why, how you use it, who you share it with, how long you keep it, and how people can access/correct their data.",
            "target_audience": "NGOs",
            "language": "en"
        },
        {
            "tip_code": "file_complaint",
            "category": "individual_rights",
            "title": "Filing a Privacy Complaint",
            "content": "If an organization violates PIPEDA, file a complaint with the Privacy Commissioner at priv.gc.ca or call 1-800-282-1376. Gather documentation first.",
            "target_audience": "citizens",
            "language": "en"
        }
    ]
    
    for tip_data in tips:
        tip = PIPEDATip(**tip_data)
        db.add(tip)
