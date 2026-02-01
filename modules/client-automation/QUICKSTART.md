# 🚀 Quick Start Guide - Enhanced Consultancy Engine

## ⚡ 60-Second Setup

### 1. Check Your API Keys
```bash
# Make sure these are in your .env file
GEMINI_API_KEY=your_key_here
BRAVE_API_KEY=your_key_here
```

### 2. Navigate to Module
```bash
cd modules/client-automation/execution
```

### 3. Run Your First Consultancy
```bash
python run_full_consultancy.py "Shopify" --industry "E-commerce"
```

**Wait 10-15 minutes and you're done!** ✅

---

## 📦 What You Just Got

After running the command, check these folders:

### Research Data
```bash
# View the comprehensive research
cat ../.tmp/research/shopify_enhanced_research.json
```

### Funding Opportunities
```bash
# See what grants they qualify for
cat ../.tmp/funding/shopify_funding.json
```

### Strategic Analysis
```bash
# Automation opportunities identified
cat ../.tmp/strategy/shopify_strategy.json
```

### Stakeholder Proposals
```bash
# 4 professional documents ready to send
ls -la ../outputs/proposals/shopify_*
```

Files created:
- `shopify_executive_summary_YYYY-MM-DD.md` → Send to CEO
- `shopify_technical_roadmap_YYYY-MM-DD.md` → Send to CTO
- `shopify_financial_model_YYYY-MM-DD.md` → Send to CFO  
- `shopify_funding_application_YYYY-MM-DD.md` → Send to grant writer

---

## 🎯 Your First Real Prospect

### Step 1: Research Phase
```bash
python run_full_consultancy.py "YourProspectName" \
  --industry "Their Industry" \
  --url "https://theirwebsite.com" \
  --location "Canada"
```

### Step 2: Review & Customize
```bash
# Read the executive summary
code ../outputs/proposals/yourprospect_executive_summary_*.md

# Customize as needed:
# - Add personal touches
# - Update specific numbers if you have insider info
# - Adjust language to match their culture
```

### Step 3: Send to Prospect
```bash
# Email structure:

Subject: [Company] - Strategic Analysis & $XXK Funding Opportunity

Hi [Name],

I conducted a strategic analysis of [Company] across 6 dimensions:
financial signals, competitive positioning, and industry trends.

Key findings:
• 3 automation opportunities → $XX,XXX annual savings
• $XX,XXX in available government funding (CDAP, SR&ED)
• Competitive gap vs [Competitor] in automation maturity

I've prepared 4 stakeholder-specific documents:
- Executive summary (attached) - for strategic review
- Technical roadmap - for your IT team  
- Financial model - for budget planning
- Funding application draft - ready to submit

Would you be open to a 15-minute call to walk through the analysis?

Best,
[Your Name]
InnovLead
```

---

## 💡 Pro Tips

### Get Better Results

**1. Always Include Industry**
```bash
# Better
python run_full_consultancy.py "Company" --industry "SaaS"

# vs Generic
python run_full_consultancy.py "Company"
```

**2. Provide URL When Possible**
```bash
python run_full_consultancy.py "Company" --url "https://company.com"
# Results in more specific insights
```

**3. Specify Location for Funding**
```bash
python run_full_consultancy.py "Company" --location "Canada"
# Gets relevant grants for their region
```

---

## 🔍 Understanding the Output

### Executive Summary
**Use for**: First email, intro calls  
**Audience**: CEO, President, Decision makers  
**Content**: Business impact, competitive advantage, ROI

### Technical Roadmap  
**Use for**: Technical validation  
**Audience**: CTO, VP Engineering, IT Director  
**Content**: Architecture, implementation phases, tech stack

### Financial Model
**Use for**: Budget approval  
**Audience**: CFO, Finance Director  
**Content**: Costs, savings, payback period, ROI

### Funding Application
**Use for**: Grant submissions  
**Audience**: Grant writer, Finance team  
**Content**: Pre-filled application with project details

---

## ⚙️ Common Scenarios

### Scenario 1: Quick Pre-Call Research
```bash
# 10 minutes before a call
python research_enhanced.py "Company Name" "Industry"

# Review key points
cat ../.tmp/research/company_enhanced_research.json | grep "pain_points"
```

### Scenario 2: Full Proposal for Warm Lead
```bash
# They're interested, need formal proposal
python run_full_consultancy.py "Company" --industry "Industry"

# Send all 4 documents
```

### Scenario 3: Funding-First Approach
```bash
# Research funding opportunities
python research_funding.py "Company" "Industry" "Canada"

# Use this as conversation starter
cat ../.tmp/funding/company_funding.json
```

---

## 🐛 Troubleshooting Quick Fixes

### "Module not found" Error
```bash
# Make sure you're in the right directory
cd modules/client-automation/execution
```

### "API Key not set" Error
```bash
# Check your .env file in project root
cat ../../../.env | grep GEMINI
cat ../../../.env | grep BRAVE
```

### "Research failed" Error
```bash
# Try with explicit URL
python run_full_consultancy.py "Company" --url "https://company.com"
```

### "Empty results"
```bash
# Check logs for details
cat ../.tmp/logs/company_consultancy_*.log
```

---

## 📊 Measuring Success

### After Each Consultancy, Track:

✅ **Research Quality**
- Did we find 5+ data points per dimension?
- Are competitors identified by name?
- Are numbers specific (not "significant growth")?

✅ **Funding Intelligence**  
- Did we find 3+ relevant programs?
- Is there an eligibility assessment?
- Are amounts estimated?

✅ **Proposal Quality**
- Is it specific to their business?
- Does it use their language/terminology?
- Is the ROI model realistic?

✅ **Business Outcome**
- Did they respond to outreach?
- Did they book a call?
- Did they move forward?

---

## 🎓 Learning Path

### Week 1: Practice
Run consultancy on 3-5 known companies to understand outputs

### Week 2: Customize
Edit proposals to match your voice and approach

### Week 3: Prospect
Use on real prospects and track response rates

### Week 4: Optimize
Update prompts based on what works

---

## 🚀 Ready to Scale?

### Automation Ideas

**1. Batch Processing**
```bash
# Create a list of prospects
for company in "Company1" "Company2" "Company3"; do
    python run_full_consultancy.py "$company" --industry "SaaS"
done
```

**2. CRM Integration**
Export results to your CRM automatically (future enhancement)

**3. Email Automation**
Connect with n8n to send proposals automatically (future enhancement)

---

## 📞 Need Help?

**Common Issues**: Check `README.md` troubleshooting section  
**Protocol Details**: Read `directives/multi_dimensional_consultancy.md`  
**Execution Logs**: Check `.tmp/logs/` for details  

---

## 🎉 You're Ready!

You now have a consultancy system that:
- ✅ Researches deeper than competitors
- ✅ Finds funding they didn't know existed  
- ✅ Creates 4 stakeholder-specific proposals
- ✅ Positions you as a strategic advisor

**Go close some deals!** 💪

---

*Remember: The consultancy IS the moat. The automation is the product. The vault is the asset.*
