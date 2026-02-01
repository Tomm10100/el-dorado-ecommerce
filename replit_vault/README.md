# 🏛️ InnovLead Vault - Replit Deployment

> The central command center for all InnovLead AI systems

---

## 🚀 Quick Deploy to Replit

### 1. Upload Files

Upload these files to your Replit project:
```
replit_vault/
├── server.py
├── requirements.txt
├── templates/
│   ├── index.html
│   ├── consultancy.html
│   ├── content.html (placeholder)
│   └── modules.html (placeholder)
└── storage/  (auto-created)
```

### 2. Configure Environment

Add to `.env` (or Replit Secrets):
```bash
GEMINI_API_KEY=your_gemini_key_here
BRAVE_API_KEY=your_brave_key_here
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Server

```bash
python server.py
```

The vault will be available at:
- **Local**: `http://localhost:5000`
- **Replit**: `https://your-repl.repl.co`

---

## 📊 What's Included

### ✅ Working Features

1. **Main Dashboard** (`/`)
   - Module overview cards
   - System health stats
   - Beautiful dark navy + electric blue theme

2. **Consultancy Engine** (`/consultancy`)
   - Form to trigger multi-dimensional analysis
   - Real-time progress monitoring
   - History of past analyses
   - Download proposals (4 types)
   - Email proposals functionality
   - Full integration with local Python modules

3. **API Endpoints** (`/api/*`)
   - `/api/consultancy/run` - Start analysis
   - `/api/consultancy/status/{job_id}` - Check progress
   - `/api/consultancy/history` - View past jobs
   - `/api/consultancy/proposals/{job_id}/{type}` - Download
   - `/api/consultancy/email/{job_id}` - Send proposals
   - `/api/modules/list` - List available modules

### 🚧 Coming Soon

- Content creation interface
- Module manager interface
- Knowledge base
- Authentication system

---

## 🔗 Integration with Local Modules

The vault connects to your local Antigravity modules:

```python
# In server.py background worker
module_path = Path(__file__).parent.parent / "modules" / "client-automation" / "execution"
script_path = module_path / "run_full_consultancy.py"

# Runs your enhanced consultancy engine
subprocess.run([sys.executable, str(script_path), company, '--industry', industry])
```

**Requirements**:
- Antigravity modules must be in `../modules/` relative to the vault
- Or update the path in `server.py` to match your setup

---

## 🎨 Theme Colors

```css
Navy 900: #0a1128  (darkest background)
Navy 800: #001f54  (cards)
Navy 700: #034078  (borders)

Electric 500: #1282A2  (primary actions)
Electric 400: #0091C7  (hover states)
Electric 300: #00B4D8  (highlights/text)
```

---

## 📧 Email Configuration

To enable auto-email functionality, add email provider setup in `server.py`:

```python
# Example using SendGrid
import sendgrid
from sendgrid.helpers.mail import Mail

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
```

Or use SMTP:
```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

# Configure your SMTP settings
```

---

## 🔒 Security Notes

### For Internal Use:

Current setup is perfect - no auth needed for closed circle

### For External/Client Access:

Add authentication:
```python
from flask import session, redirect
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/consultancy')
@login_required
def consultancy_page():
    return render_template('consultancy.html')
```

---

## 🐛 Troubleshooting

### "Module not found" errors
```bash
# Make sure you're in the correct directory
cd replit_vault
python server.py
```

### Consultancy fails to run
```bash
# Check module path is correct
# Edit server.py line ~340:
module_path = Path(__file__).parent.parent / "modules" / "client-automation" / "execution"
```

### Proposals not downloading
```bash
# Ensure proposals are being saved to correct location
# Check storage/proposals/ directory exists
```

---

## 📈 Scaling Tips

### Use Replit DB Instead of In-Memory

```python
from replit import db

# Replace vault_db dict with Replit DB
vault_db['consultancy_jobs'][job_id] = job_data
# becomes
db[f"consultancy:{job_id}"] = json.dumps(job_data)
```

### Add Redis for Job Queue

```python
import redis
r = redis.from_url(os.environ.get('REDIS_URL'))

# Use for background job processing
r.lpush('consultancy_queue', job_id)
```

### Deploy Workers Separately

For production, run background workers as separate processes:
```bash
# Terminal 1: Web server
python server.py

# Terminal 2: Worker
python worker.py
```

---

## 🎯 Usage Flow

1. **User visits** https://your-vault.repl.co
2. **Clicks** "Consultancy Engine" card
3. **Fills form** with company details
4. **Clicks** "Run Full Consultancy"
5. **Watches progress** bar (10-15 min)
6. **Views results** with metrics
7. **Downloads or emails** 4 proposals

---

## 💻 Local Development

```bash
# Clone your Antigravity project
cd Antigravity/replit_vault

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY=your_key
export BRAVE_API_KEY=your_key

# Run
python server.py
```

Visit http://localhost:5000

---

## 📞 Support

Issues? Check:
1. `storage/logs/` for execution logs
2. Browser console for JavaScript errors
3. Terminal output for server errors

---

**Built with ❤️ for InnovLead**

*The consultancy is the moat. The automation is the product. The vault is the asset.*
