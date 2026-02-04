
import os

file_path = r'c:\Users\Ryzen 9 5900X\Desktop\Antigravity\el-dorado-site\src\style.css'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix selector mismatch
new_content = content.replace('.hero-section {', '#hero {')
# Fix height locking on mobile (add height: auto rule)
new_content = new_content.replace('min-height: 100vh;', 'min-height: 100vh; height: auto;')

if content == new_content:
    print("No changes made. Pattern not found?")
else:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully patched style.css")
