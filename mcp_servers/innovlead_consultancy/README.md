# 🎯 InnovLead Consultancy MCP Server

> **AI-Native Consultancy Automation via Model Context Protocol**

This MCP server exposes InnovLead's multi-dimensional consultancy system to AI assistants, enabling conversational automation of the entire client analysis pipeline.

---

## 🚀 What It Does

Transform manual consultancy workflows into AI-orchestrated automation:

**Before (Manual)**:
```bash
cd modules/client-automation/execution
py run_full_consultancy.py "Tesla" --industry "Automotive"
# Wait 10-15 minutes...
# Check outputs/proposals/ folder
# Manually email files to client
```

**After (AI-Powered)**:
```
You: "Run a consultancy for Tesla in automotive"

AI: "Starting analysis... 
     [15 seconds later]
     ✅ Research complete - 3 competitors identified
     ✅ Funding found - $45K IRAP + $25K provincial
     ✅ Strategy generated - 5 opportunities, $120K ROI
     ✅ 4 proposals created
     
     Want me to send the executive summary to their CEO?"
```

---

## 📦 Available Tools

### 1. **run_full_consultancy**
Execute complete multi-dimensional analysis

**Input**:
- `company` (required): Company name
- `industry` (optional): Industry sector  
- `url` (optional): Company website
- `location` (optional): Geographic location (default: "Canada")

**Output**: Job ID for tracking

**Example**:
```json
{
  "company": "Shopify",
  "industry": "E-commerce",
  "url": "https://shopify.com",
  "location": "Canada"
}
```

---

### 2. **check_consultancy_status**
Monitor progress of running job

**Input**:
- `job_id` (required): Job ID from run_full_consultancy

**Output**: Status, progress %, phase

**Example**:
```json
{
  "job_id": "job_20260126_143000_tesla"
}
```

---

### 3. **get_consultancy_results**
Retrieve completed analysis data

**Input**:
- `job_id` (required): Job ID

**Output**: Full results with metrics and file paths

---

### 4. **download_proposal**
Get specific proposal document

**Input**:
- `job_id` (required): Job ID
- `proposal_type` (required): One of:
  - `executive` - Executive summary (CEO/President)
  - `technical` - Technical roadmap (CTO/IT)
  - `financial` - Financial model (CFO)
  - `funding` - Funding application (Grant writer)

**Output**: Proposal content

---

### 5. **send_proposals_email**
Email proposals to client (placeholder)

**Input**:
- `job_id` (required): Job ID
- `recipient_email` (required): Email address
- `proposals` (optional): List of proposal types to send

**Note**: Requires email service configuration

---

### 6. **list_consultancy_history**
View all past analyses

**Input**: None

**Output**: List of all jobs with status

---

## 🗂️ Resources

### consultancy://history
Historical record of all consultancy analyses

### consultancy://templates
Available proposal templates and formats

---

## 🛠️ Setup

### 1. Install Dependencies
```bash
py -m pip install mcp uvicorn starlette pydantic
```

### 2. Verify Module Path
Ensure `modules/client-automation/execution/run_full_consultancy.py` exists

### 3. Run Server
```bash
py mcp_servers/innovlead_consultancy/server.py
```

### 4. Connect Antigravity
The server will automatically be available to Cline AI assistant

---

## 💡 Usage Examples

### Example 1: New Lead Analysis
```
You: "New lead: Acme Corp, manufacturing"

AI uses: run_full_consultancy
  → company="Acme Corp"
  → industry="Manufacturing"
  → Returns job_id

AI uses: check_consultancy_status (periodically)
  → Monitors progress

AI uses: get_consultancy_results
  → Retrieves findings

AI: "Analysis complete! Found $35K in grants and 
     3 automation opportunities worth $150K/year.
     Want to see the executive summary?"
```

### Example 2: Checking Past Work
```
You: "What consultancies did we run this week?"

AI uses: list_consultancy_history
  → Gets all jobs

AI: "5 consultancies this week:
     - Tesla (complete, $75K funding found)
     - Shopify (running, 80% done)
     - Nike (complete, proposals sent)
     - Microsoft (error, needs retry)
     - Apple (complete)"
```

### Example 3: Downloading Proposal
```
You: "Get me the Tesla executive summary"

AI uses: list_consultancy_history
  → Finds Tesla job_id

AI uses: download_proposal
  → job_id="job_20260126_tesla"
  → proposal_type="executive"

AI: [Returns full executive summary content]
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│  You (Natural Language)                     │
└─────────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  Cline AI Assistant                         │
│  • Understands intent                       │
│  • Calls appropriate MCP tools              │
│  • Formats results                          │
└─────────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  InnovLead Consultancy MCP Server           │
│  • Exposes 6 tools                          │
│  • Manages job queue                        │
│  • Executes Python scripts                  │
└─────────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  Your Existing Modules                      │
│  • run_full_consultancy.py                  │
│  • research_enhanced.py                     │
│  • research_funding.py                      │
│  • generate_proposal_suite.py               │
└─────────────────────────────────────────────┘
```

---

## 📊 Job Lifecycle

1. **Created** - Job record created, queued
2. **Running** - Python script executing
   - Phase: research → funding → strategy → proposals
   - Progress: 0% → 25% → 50% → 75% → 100%
3. **Complete** - All outputs generated
4. **Error** - Something failed (check logs)

---

## 🔍 Troubleshooting

### "Job not found"
- Job ID might be incorrect
- Use `list_consultancy_history` to find correct ID

### "Job not complete"
- Analysis still running (10-15 min typical)
- Use `check_consultancy_status` to monitor
- Check for errors if stuck

### "Proposal file not found"
- Job might have failed silently
- Check `modules/client-automation/.tmp/logs/`
- Verify output files exist in `outputs/proposals/`

### "Module not found"
- Verify Python path includes project root
- Check `MODULES_PATH` in server.py is correct
- Ensure all dependencies installed

---

## 🚀 Production Deployment

For 24/7 availability:

### Option 1: Local (Current)
- Runs on your machine
- Free, full control
- Only available when you're working

### Option 2: Cloud Hosting
Deploy to Railway/Render/Fly.io:
```bash
# Add to Procfile
web: py mcp_servers/innovlead_consultancy/server.py
```

Configure:
- Environment variables
- Database (replace in-memory jobs_db)
- Authentication
- Monitoring

---

## 🔒 Security Considerations

**Current (Local)**:
- ✅ No external access
- ✅ No auth needed
- ✅ Your API keys stay local

**Production (Cloud)**:
- ⚠️ Add authentication
- ⚠️ Encrypt sensitive data
- ⚠️ Rate limiting
- ⚠️ Audit logging

---

## 📈 Metrics & Monitoring

Track in production:
- Jobs per day
- Success vs error rate
- Average execution time
- Most common industries
- Funding amounts identified
- Proposal download rates

---

## 🎯 Future Enhancements

- [ ] Real-time progress streaming
- [ ] Email integration (SendGrid/SMTP)
- [ ] CRM synchronization
- [ ] Webhook notifications
- [ ] Multi-company batch processing
- [ ] Custom proposal templates
- [ ] Analytics dashboard
- [ ] Proposal versioning

---

## 📞 Support

**Issues?**
1. Check server logs
2. Verify module paths
3. Test with `py modules/client-automation/execution/run_full_consultancy.py "Test Company"`
4. Review `modules/client-automation/.tmp/logs/`

**Questions?**
Refer to main consultancy documentation:
- `modules/client-automation/README.md`
- `modules/client-automation/directives/multi_dimensional_consultancy.md`

---

**Built for AI-native automation** 🚀  
**Making consultancy conversational**
