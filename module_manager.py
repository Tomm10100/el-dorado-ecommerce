"""
Antigravity Module Manager
CLI tool to manage platform modules

Usage:
    py module_manager.py list
    py module_manager.py run content-creation "Topic Name"
    py module_manager.py status content-creation
    py module_manager.py create new-module-name
"""

import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict


class ModuleManager:
    """Manage Antigravity modules"""
    
    def __init__(self):
        self.root = Path(__file__).parent
        self.registry_path = self.root / "core" / "config" / "module_registry.json"
        self.modules_dir = self.root / "modules"
        self.registry = self._load_registry()
    
    def _load_registry(self) -> Dict:
        """Load module registry"""
        if not self.registry_path.exists():
            return {"modules": []}
        
        with open(self.registry_path, 'r') as f:
            return json.load(f)
    
    def _save_registry(self):
        """Save module registry"""
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=2)
    
    def list_modules(self):
        """List all registered modules"""
        print("\n Antigravity Modules:")
        print("=" * 60)
        
        for module in self.registry.get("modules", []):
            status_icon = "" if module["status"] == "active" else ""
            print(f"{status_icon} {module['name']} (v{module['version']})")
            print(f"   Path: {module['path']}")
            print(f"   Entry: {module['entry_point']}")
            print()
        
        print(f"Total modules: {len(self.registry.get('modules', []))}\n")
    
    def run_module(self, module_name: str, *args):
        """Run a module's entry point"""
        module = self._find_module(module_name)
        
        if not module:
            print(f" Module '{module_name}' not found")
            return
        
        module_path = self.root / module["path"]
        entry_script = module_path / module["entry_point"]
        
        if not entry_script.exists():
            print(f" Entry point not found: {entry_script}")
            return
        
        print(f" Running {module_name}...")
        print(f"   Script: {entry_script}")
        print()
        
        # Run the module
        cmd = [sys.executable, str(entry_script)] + list(args)
        subprocess.run(cmd, cwd=str(module_path))
    
    def status(self, module_name: str):
        """Show module status and details"""
        module = self._find_module(module_name)
        
        if not module:
            print(f" Module '{module_name}' not found")
            return
        
        module_path = self.root / module["path"]
        metadata_file = module_path / "module.json"
        
        print(f"\n Module: {module_name}")
        print("=" * 60)
        print(f"Status: {module['status']}")
        print(f"Version: {module['version']}")
        print(f"Path: {module['path']}")
        print(f"Entry Point: {module['entry_point']}")
        
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            print(f"\nDescription: {metadata.get('description', 'N/A')}")
            print(f"Dependencies: {', '.join(metadata.get('dependencies', []))}")
            print(f"APIs Used: {', '.join(metadata.get('apis_used', []))}")
        
        print()
    
    def create_module(self, module_name: str):
        """Create a new module from template"""
        module_path = self.modules_dir / module_name
        
        if module_path.exists():
            print(f" Module '{module_name}' already exists")
            return
        
        print(f" Creating module: {module_name}")
        
        # Create structure
        (module_path / "directives").mkdir(parents=True)
        (module_path / "execution").mkdir(parents=True)
        (module_path / ".tmp").mkdir(parents=True)
        (module_path / "outputs").mkdir(parents=True)
        
        # Create README
        readme_content = f"""# {module_name.title().replace('-', ' ')} Module

## Description
[Add module description here]

## Usage
```bash
py module_manager.py run {module_name}
```

## Directives
- Add your SOPs in `directives/`

## Execution Scripts
- Add your Python scripts in `execution/`
"""
        (module_path / "README.md").write_text(readme_content)
        
        # Create module.json
        metadata = {
            "name": module_name,
            "version": "0.1.0",
            "description": "New module (update description)",
            "status": "inactive",
            "dependencies": ["core.lib.logger"],
            "mcp_servers": [],
            "entry_point": "execution/main.py",
            "author": "InnovLead",
            "last_updated": "2025-12-11"
        }
        
        with open(module_path / "module.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Add to registry
        self.registry["modules"].append({
            "name": module_name,
            "path": f"modules/{module_name}",
            "status": "inactive",
            "version": "0.1.0",
            "entry_point": "execution/main.py"
        })
        self._save_registry()
        
        print(f" Module created: {module_path}")
        print(f"   Next: Add directives and execution scripts")
    
    def _find_module(self, name: str) -> Dict:
        """Find module by name"""
        for module in self.registry.get("modules", []):
            if module["name"] == name:
                return module
        return None


def main():
    manager = ModuleManager()
    
    if len(sys.argv) < 2:
        print("\n Antigravity Module Manager")
        print("\nUsage:")
        print("  py module_manager.py list")
        print("  py module_manager.py run <module-name> [args...]")
        print("  py module_manager.py status <module-name>")
        print("  py module_manager.py create <module-name>")
        return
    
    command = sys.argv[1]
    
    if command == "list":
        manager.list_modules()
    
    elif command == "run":
        if len(sys.argv) < 3:
            print(" Usage: py module_manager.py run <module-name> [args...]")
            return
        manager.run_module(sys.argv[2], *sys.argv[3:])
    
    elif command == "status":
        if len(sys.argv) < 3:
            print(" Usage: py module_manager.py status <module-name>")
            return
        manager.status(sys.argv[2])
    
    elif command == "create":
        if len(sys.argv) < 3:
            print(" Usage: py module_manager.py create <module-name>")
            return
        manager.create_module(sys.argv[2])
    
    else:
        print(f" Unknown command: {command}")
        print("   Available: list, run, status, create")


if __name__ == "__main__":
    main()

