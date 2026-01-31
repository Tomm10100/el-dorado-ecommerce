"""
Replit DB MCP Connector
Key-value database for client data and automation tracking
"""

import os
from typing import Any, Dict, List, Optional
from pathlib import Path

try:
    from replit import db
    REPLIT_DB_AVAILABLE = True
except ImportError:
    REPLIT_DB_AVAILABLE = False
    # Fallback to local JSON for development
    import json


class ReplitDBMCP:
    """MCP for Replit Database (key-value store)"""
    
    def __init__(self):
        if REPLIT_DB_AVAILABLE:
            self.db = db
            self.storage_type = "replit-db"
        else:
            # Local JSON fallback for development
            self.db_file = Path(".tmp/local_db.json")
            self.db_file.parent.mkdir(exist_ok=True)
            self._load_local()
            self.storage_type = "local-json"
    
    def _load_local(self):
        """Load local JSON database"""
        if self.db_file.exists():
            with open(self.db_file, 'r') as f:
                self._local_data = json.load(f)
        else:
            self._local_data = {}
    
    def _save_local(self):
        """Save local JSON database"""
        with open(self.db_file, 'w') as f:
            json.dump(self._local_data, f, indent=2)
    
    def set(self, key: str, value: Any) -> bool:
        """Set a value in the database"""
        try:
            if REPLIT_DB_AVAILABLE:
                self.db[key] = value
            else:
                self._local_data[key] = value
                self._save_local()
            return True
        except Exception as e:
            print(f"Error setting {key}: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the database"""
        try:
            if REPLIT_DB_AVAILABLE:
                return self.db.get(key, default)
            else:
                return self._local_data.get(key, default)
        except Exception as e:
            print(f"Error getting {key}: {e}")
            return default
    
    def delete(self, key: str) -> bool:
        """Delete a key from the database"""
        try:
            if REPLIT_DB_AVAILABLE:
                del self.db[key]
            else:
                if key in self._local_data:
                    del self._local_data[key]
                    self._save_local()
            return True
        except Exception as e:
            print(f"Error deleting {key}: {e}")
            return False
    
    def list_keys(self, prefix: str = "") -> List[str]:
        """List all keys, optionally filtered by prefix"""
        try:
            if REPLIT_DB_AVAILABLE:
                return [k for k in self.db.keys() if k.startswith(prefix)]
            else:
                return [k for k in self._local_data.keys() if k.startswith(prefix)]
        except Exception as e:
            print(f"Error listing keys: {e}")
            return []
    
    # Helper methods for common patterns
    
    def get_client(self, client_name: str) -> Optional[Dict]:
        """Get client data"""
        return self.get(f"client:{client_name}")
    
    def save_client(self, client_name: str, data: Dict) -> bool:
        """Save client data"""
        return self.set(f"client:{client_name}", data)
    
    def log_automation_run(self, module: str, status: str, details: Dict) -> bool:
        """Log an automation run"""
        from datetime import datetime
        log_entry = {
            "module": module,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            **details
        }
        
        # Append to logs
        logs = self.get(f"logs:{module}", [])
        logs.append(log_entry)
        
        # Keep only last 100 entries
        if len(logs) > 100:
            logs = logs[-100:]
        
        return self.set(f"logs:{module}", logs)
    
    def get_automation_logs(self, module: str, limit: int = 10) -> List[Dict]:
        """Get recent automation logs"""
        logs = self.get(f"logs:{module}", [])
        return logs[-limit:]


# Quick test
if __name__ == "__main__":
    mcp = ReplitDBMCP()
    
    print(f"Using: {mcp.storage_type}")
    
    # Test basic operations
    mcp.set("test_key", {"value": 123})
    print(f"Get test: {mcp.get('test_key')}")
    
    # Test client storage
    mcp.save_client("ABC Corp", {
        "industry": "Tech",
        "status": "active",
        "contact": "john@abc.com"
    })
    
    print(f"Client data: {mcp.get_client('ABC Corp')}")
    
    # Test logging
    mcp.log_automation_run("content-creation", "success", {
        "topic": "AI",
        "duration": 45
    })
    
    print(f"Logs: {mcp.get_automation_logs('content-creation')}")
    
    print("\n✅ Replit DB MCP working!")
