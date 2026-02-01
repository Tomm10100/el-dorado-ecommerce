# MCP Integrations Module

**Layer 3 of Antigravity: The Context Layer**

## 🧠 What is this?
This module provides Antigravity with "senses" - the ability to observe, remember, and act on external systems via the Model Context Protocol (MCP).

## 🔌 Connected Capabilities

| Connector | Status | Purpose | Capabilities |
|-----------|--------|---------|--------------|
| **Replit DB** | ✅ Ready | **Memory** | Store client data, logs, key-value automated memory |
| **Replit FS** | ✅ Ready | **Vision** | Insect/modify deployed code in Repls, check health |
| **Brave Search** | ✅ Ready | **Research** | Unrestricted web research, competitive analysis |
| **n8n Cloud** | ✅ Ready | **Action** | Create, trigger, and monitor automation workflows |

## 🛠️ Usage

### Python Execution
```python
from modules.mcp_integrations.execution.replit_db_connector import ReplitDBMCP
from modules.mcp_integrations.execution.n8n_connector import N8nCloudMCP

# 1. Remember something
mem = ReplitDBMCP()
mem.save_client("Tesla", {"status": "prospect"})

# 2. Trigger Action
n8n = N8nCloudMCP()
n8n.trigger_workflow_by_name("send-email", {"to": "elon@tesla.com"})
```

### CLI Testing
Run the diagnostic suite to check all connections:
```bash
py execution/test_all_mcps.py
```

## 🔐 Credentials Required

Add these to your root `.env` file:

```bash
# Replit (Free)
REPLIT_TOKEN=your_token

# Web Research (~$20/mo)
BRAVE_API_KEY=your_key

# n8n Cloud (Existing Plan)
N8N_API_KEY=your_key
N8N_BASE_URL=https://your-instance.app.n8n.cloud
```

## 🏗️ Architecture

- **`execution/`**: Python classes for each service
- **`directives/`**: SOPs on *when* to use which sense
- **`.tmp/`**: Local caching (e.g., local DB fallback)

## 🚀 Future Integrations
- GitHub MCP (Code repos)
- Stripe MCP (Payments)
- OpenAI MCP (Additional reasoning)
