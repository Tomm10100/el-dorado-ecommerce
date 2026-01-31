# Fix Unicode characters in run_full_consultancy.py

with open('modules/client-automation/execution/run_full_consultancy.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace corrupted characters with ASCII equivalents
content = content.replace('\u2713', '[OK]')  # checkmark
content = content.replace('\u2717', '[X]')   # X mark
content = content.replace('\U0001f4c1', '[FILES]')  # folder emoji
content = content.replace('\U0001f4ca', '[LOG]')    # bar chart emoji
content = content.replace('\U0001f3af', '[NEXT]')   # target emoji
content = content.replace('\u2022', '*')     # bullet point
content = content.replace('\u2192', '->')    # arrow

# Also handle any malformed UTF-8
import re
# Remove any remaining non-ASCII characters in log messages
content = re.sub(r'[^\x00-\x7F]+', '', content)

with open('modules/client-automation/execution/run_full_consultancy.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed!")
