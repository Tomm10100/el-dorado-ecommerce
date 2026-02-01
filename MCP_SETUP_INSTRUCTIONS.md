# 🚀 MCP Server Setup - Quick Instructions

## ✅ **What's Done**

1. ✅ MCP SDK installed
2. ✅ Consultancy MCP Server built (fixed startup code)
3. ✅ Configuration file created: `mcp_settings.json`

---

## 🔧 **Final Setup Steps**

### **Option 1: Configure Antigravity MCP Settings (Recommended)**

Antigravity needs to know about your MCP server. Here's how:

1. **Open Antigravity Settings**
   - Look for Settings/Preferences menu
   - Find "MCP Servers" or "Extensions" section

2. **Add the MCP Server Configuration**
   
   Copy this configuration:
   ```json
   {
     "mcpServers": {
       "innovlead-consultancy": {
         "command": "py",
         "args": [
           "c:\\Users\\Ryzen 9 5900X\\Desktop\\Antigravity\\mcp_servers\\innovlead_consultancy\\server.py"
         ],
         "env": {}
       }
     }
   }
   ```
   
   Or point Antigravity to the file: `c:\Users\Ryzen 9 5900X\Desktop\Antigravity\mcp_settings.json`

3. **Restart Antigravity** (if needed)

---

### **Option 2: If Antigravity Has a Config File**

Some AI assistants use a config file like:
- `~/.config/antigravity/mcp.json`
- `%APPDATA%/Antigravity/mcp_settings.json`
- Or in the Antigravity installation directory

**Add this to that file**:
```json
{
  "mcpServers": {
    "innovlead-consultancy": {
      "command": "py",
      "args": [
        "c:\\Users\\Ryzen 9 5900X\\Desktop\\Antigravity\\mcp_servers\\innovlead_consultancy\\server.py"
      ],
      "env": {}
    }
  }
}
```

---

## 🧪 **How to Test**

Once configured, ask me (Cline):

```
"What MCP tools do you have access to?"
```

**Expected Result**: I should list these 6 tools:
- ✅ run_full_consultancy
- ✅ check_consultancy_status  
- ✅ get_consultancy_results
- ✅ download_proposal
- ✅ send_proposals_email
- ✅ list_consultancy_history

---

## 🎯 **Simple Test**

Once tools are available, try:

```
"Run a consultancy for a test company called 'Test Corp' in the tech industry"
```

I should:
1. Start the analysis via MCP
2. Return a job ID
3. You can then check status

---

## 🔍 **Troubleshooting**

### **If I don't see the tools:**

1. **Check Antigravity logs** - Look for MCP server errors
2. **Verify Python path** - Run: `py --version` (should work)
3. **Test server manually**:
   ```bash
   py mcp_servers/innovlead_consultancy/server.py
   ```
   Should start without errors (will wait for input)

### **If server won't start:**

- Make sure all dependencies installed: `py -m pip install -r requirements.txt`
- Check the path in mcp_settings.json is correct
- Verify no syntax errors in server.py

---

## 📞 **Need Help?**

1. Share any error messages you see
2. Check Antigravity documentation for MCP configuration
3. The MCP server is ready - just needs to be connected!

---

## 🎉 **Once Working**

You'll be able to:
- **Run consultancies conversationally**: "Run analysis for Tesla"
- **Check status naturally**: "How's the Tesla analysis going?"
- **Get proposals**: "Show me the executive summary"
- **View history**: "What companies did we analyze?"

**No more manual script running!** 🚀

---

**Next**: Configure Antigravity to connect to the MCP server, then we're live!
