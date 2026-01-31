import os
import base64
from pathlib import Path

# Paths
SOURCE_DIR = Path("replit_vault/consultancy_bot")
OUTPUT_FILE = Path("install_consultancy_bot.py")

def generate_installer():
    if not SOURCE_DIR.exists():
        print(f"Error: {SOURCE_DIR} does not exist")
        return

    # Header for the installer script
    installer_content = [
        '"""',
        'InnovLead Vault - ConsultancyBot Installer',
        'Run this script in Replit to install/upgrade the ConsultancyBot package.',
        '"""',
        'import os',
        'import base64',
        'from pathlib import Path',
        '',
        '# File contents (Base64 encoded)',
        'FILES = {'
    ]

    # Walk through directory
    print(f"Scanning {SOURCE_DIR}...")
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            file_path = Path(root) / file
            
            # Skip pycache and hidden files
            if "__pycache__" in str(file_path):
                continue
                
            # Read file content
            with open(file_path, 'rb') as f:
                content = f.read()
                
            # Base64 encode
            b64_content = base64.b64encode(content).decode('utf-8')
            
            # Relative path for the installer
            relative_path = file_path.as_posix() # Ensure forward slashes
            
            installer_content.append(f'    "{relative_path}": "{b64_content}",')
            print(f"  Packed: {relative_path}")

    # Footer for the installer script
    installer_content.extend([
        '}',
        '',
        'def install():',
        '    print("🚀 Installing ConsultancyBot...")',
        '    ',
        '    for file_path, b64_content in FILES.items():',
        '        # Create directory',
        '        path = Path(file_path)',
        '        path.parent.mkdir(parents=True, exist_ok=True)',
        '        ',
        '        # Decode and write',
        '        content = base64.b64decode(b64_content)',
        '        with open(path, "wb") as f:',
        '            f.write(content)',
        '        ',
        '        print(f"  ✓ Installed: {file_path}")',
        '    ',
        '    print("\\n✅ Installation Complete!")',
        '    print("Now update your server.py to use the new module.")',
        '',
        'if __name__ == "__main__":',
        '    install()'
    ])

    # Write the installer file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(installer_content))
    
    print(f"\nInstaller generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_installer()
