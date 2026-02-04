
import os

file_path = r'c:\Users\Ryzen 9 5900X\Desktop\Antigravity\el-dorado-site\src\style.css'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix order and margin for frequency controls
target = """/* Resonance UI - Centered Bottom */
.frequency-controls {
  position: relative; /* No longer absolute left */
  top: auto;
  left: auto;
  transform: none;
  z-index: 5;
  order: 3; /* Controls Bottom */
  margin-top: 4rem; /* Pushed lower as requested */
}"""

replacement = """/* Resonance UI - Centered Bottom */
.frequency-controls {
  position: relative; /* No longer absolute left */
  top: auto;
  left: auto;
  transform: none;
  z-index: 5;
  order: 4; /* Controls Bottom (Below visualizer) */
  margin-top: 1rem;
}"""

if target in content:
    new_content = content.replace(target, replacement)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully updated frequency controls order")
else:
    print("Target block not found precisely. Manual check needed.")
