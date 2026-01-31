# 🔌 InnovLead MCP Servers

> **AI-Native Automation Infrastructure for InnovLead Vault**

This directory contains MCP (Model Context Protocol) servers that expose InnovLead's automation capabilities to AI assistants.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│  AI Assistant (Cline)                                   │
│  • Natural language commands                            │
│  • Workflow orchestration                               │
│  • Error handling                                       │
└─────────────────────────────────────────────────────────┘
                          ↓
        ┌─────────────────┴─────────────────┬─────────────────┐
        ↓                                    ↓                 ↓
┌──────────────────┐              ┌──────────────────┐  ┌──────────────────┐
│ Consultancy      │              │ Content          │  │ Memory           │
│ MCP Server       │              │ MCP Server       │  │ MCP Server       │
│                  │              │                  │  │                  │
│ Port: 3001       │              │ Port: 3002       │  │ Port: 3003       │
└──────────────────┘              └──────────────────┘  └──────────────────┘
        ↓                                    ↓                 ↓
┌─────────────────────────────────────────────────────────────┐
│  InnovLead Modules (Python)                                 │
│  • modules/client-automation/                               │
│  • modules/content-creation/                                │
│  • Filesystem & Database                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Available MCP Servers

### 1. **InnovLead Consultancy** (`innovlead_consultancy/`)
**Purpose**: Automate full multi-dimensional client consultancy pipeline

**Tools**:
- `run_full_consultancy` - Execute complete analysis (research, funding, strategy, proposals)
- `check_consultancy_status` - Monitor progress of running consultancy
- `get_consultancy_results` - Retrieve analysis data and metrics
- `download_proposal` - Get specific proposal document
- `send_proposals_email` - Email proposals to client
- `list_consultancy_history` - View all past analyses

**Resources**:
- `consultancy://history` - Historical consultancy data
- `consultancy://templates` - Proposal templates
- `consultancy://funding-database` - Available grants/programs

---

### 2. **InnovLead Content** (`innovlead_content/`)
**Purpose**: Automated content creation and social media publishing

**Tools**:
- `discover_trending_topics` - Find what's hot in tech
- `generate_content_post` - Create ELI5 post + infographic
- `publish_to_social` - Post to Instagram/TikTok
- `schedule_post` - Queue for later publishing
- `analyze_performance` - Get engagement metrics

**Resources**:
- `content://library` - All generated content
- `content://calendar` - Publishing schedule
- `content://analytics` - Performance data

---

### 3. **InnovLead Memory** (`innovlead_memory/`)
**Purpose**: Persistent storage and data access layer

**Tools**:
- `save_client_data` - Store client information
- `get_client_data` - Retrieve client profile
- `update_client_status` - Change pipeline status
- `log_activity` - Record system actions
- `search_clients` - Find clients by criteria

**Resources**:
- `memory://clients` - All client profiles
- `memory://logs` - System activity logs
- `memory://config` - System configuration

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
py -m pip install mcp uvicorn starlette
```

### 2. Start MCP Servers
```bash
# Start all servers
py mcp_servers/start_all.py

# Or individually
py mcp_servers/innovlead_consultancy/server.py
py mcp_servers/innovlead_content/server.py
py mcp_servers/innovlead_memory/server.py
```

### 3. Configure Antigravity
Add servers to Antigravity's MCP configuration (handled automatically)

### 4. Use Conversationally
```
You: "Run a consultancy for Tesla"
AI: *[Uses MCP] → Executes → Returns results*

You: "Generate today's content post"
AI: *[Uses MCP] → Creates → Publishes*
```

---

## 🛠️ Development

### Server Structure
```
innovlead_consultancy/
├── __init__.py              # Package init
├── server.py                # Main MCP server
├── tools.py                 # Tool implementations
├── resources.py             # Resource providers
├── config.json              # Server configuration
└── README.md                # Documentation
```

### Adding a New Tool
```python
# In tools.py
@server.tool()
async def your_new_tool(param: str) -> dict:
    """Tool description"""
    # Implementation
    return {"result": "data"}
```

### Adding a New Resource
```python
# In resources.py
@server.resource("consultancy://your-resource")
async def your_resource() -> dict:
    """Resource description"""
    # Implementation
    return {"data": [...]}
```

---

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:3001/health
curl http://localhost:3002/health
curl http://localhost:3003/health
```

### Logs
Check `logs/` directory for server execution logs

---

## 🔒 Security

- MCP servers run locally (not exposed to internet by default)
- For production deployment, add authentication
- Use environment variables for sensitive data

---

## 🎯 Production Deployment

For 24/7 availability:
1. Deploy to Railway, Render, or Fly.io
2. Add proper authentication
3. Configure HTTPS
4. Monitor with health checks

---

**Built for AI-native automation** 🚀
