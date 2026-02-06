# 🚀 InnovLead Education Bot - Deployment Guide

Complete guide to deploying and running the InnovLead Universal AI Education Bot.

---

## 📋 Prerequisites

### Required
- Python 3.9 or higher
- Telegram account
- Anthropic API key (Claude) **OR** OpenAI API key
- Telegram Bot Token from [@BotFather](https://t.me/botfather)

### Optional
- PostgreSQL database (for production)
- n8n instance (for automation workflows)
- Domain name (for webhook mode)

---

## 🛠️ Installation Steps

### 1. Clone or Download the Repository

```bash
cd innovlead-education-bot
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Get Your Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the prompts to create your bot
4. Copy the bot token (looks like `123456:ABC-DEF...`)
5. Set bot commands using `/setcommands`:

```
start - Welcome & registration
aprender - Access learning modules
privacidad - Quick PIPEDA privacy tips
progreso - View your progress
ayuda - Help & support
```

### 5. Get AI Provider API Key

**Option A: Anthropic Claude (Recommended)**
1. Visit [console.anthropic.com](https://console.anthropic.com)
2. Create account or sign in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key

**Option B: OpenAI**
1. Visit [platform.openai.com](https://platform.openai.com)
2. Create account or sign in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key

### 6. Configure Environment Variables

Copy the example environment file:
```bash
copy .env.example .env
```

Edit `.env` with your actual values:

```env
# REQUIRED: Telegram Bot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# REQUIRED: AI Provider (choose one)
ANTHROPIC_API_KEY=your_anthropic_key_here
AI_PROVIDER=anthropic

# OR use OpenAI
# OPENAI_API_KEY=your_openai_key_here
# AI_PROVIDER=openai

# RECOMMENDED: Security
SECRET_KEY=generate_a_random_secret_key_here
ENVIRONMENT=production

# OPTIONAL: Database (uses SQLite by default)
DATABASE_URL=sqlite:///innovlead_bot.db

# OPTIONAL: Logging
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
```

**Generate a secure secret key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 7. Initialize Database

```bash
python -m database.init_db
```

You should see:
```
✅ Database initialized successfully!
✅ Seeded modules, lessons, and PIPEDA tips
✅ Database setup complete!
```

### 8. Test the Bot

```bash
python -m bot.main
```

You should see:
```
======================================================================
🎓 InnovLead Universal AI Education Bot
======================================================================
✅ Bot is running in polling mode
✅ AI Tutor: Enabled
✅ Organization: InnovLead Foundation
✅ Environment: development

💡 Press Ctrl+C to stop the bot
======================================================================
```

### 9. Test on Telegram

1. Open Telegram
2. Search for your bot by username
3. Send `/start` command
4. You should receive a welcome message!

---

## 🔧 Configuration Options

### Bot Mode

**Polling Mode (Development):**
```env
BOT_MODE=polling
```
- Bot actively checks for new messages
- Easy to set up
- Good for development and testing

**Webhook Mode (Production):**
```env
BOT_MODE=webhook
WEBHOOK_URL=https://yourdomain.com
WEBHOOK_PORT=8443
```
- Telegram sends updates to your server
- More efficient for high traffic
- Requires HTTPS domain

### AI Provider

**Anthropic Claude:**
```env
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_key
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

**OpenAI:**
```env
AI_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4-turbo-preview
```

### Database

**SQLite (Default - Development):**
```env
DATABASE_URL=sqlite:///innovlead_bot.db
```

**PostgreSQL (Production):**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/innovlead_bot
```

**Supabase:**
```env
DATABASE_URL=postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres
```

### Feature Flags

```env
ENABLE_AI_TUTOR=true
ENABLE_QUIZZES=true
ENABLE_CERTIFICATES=true
ENABLE_COMMUNITY=false
```

---

## 🌐 Production Deployment

### Option 1: VPS (DigitalOcean, Linode, AWS EC2)

1. **Provision Server**
   - Ubuntu 22.04 LTS recommended
   - Minimum 1GB RAM

2. **Install Dependencies**
```bash
sudo apt update
sudo apt install python3.9 python3-pip python3-venv git -y
```

3. **Clone Repository**
```bash
git clone https://github.com/innovlead-foundation/education-bot.git
cd innovlead-education-bot
```

4. **Set up Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. **Configure .env**
```bash
cp .env.example .env
nano .env  # Edit with your values
```

6. **Initialize Database**
```bash
python -m database.init_db
```

7. **Run with systemd**

Create `/etc/systemd/system/innovlead-bot.service`:

```ini
[Unit]
Description=InnovLead Education Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/innovlead-education-bot
Environment="PATH=/path/to/innovlead-education-bot/venv/bin"
ExecStart=/path/to/innovlead-education-bot/venv/bin/python -m bot.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable innovlead-bot
sudo systemctl start innovlead-bot
sudo systemctl status innovlead-bot
```

### Option 2: Docker

**Dockerfile** (create this):
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -m database.init_db

CMD ["python", "-m", "bot.main"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  bot:
    build: .
    env_file: .env
    volumes:
      - ./logs:/app/logs
      - ./innovlead_bot.db:/app/innovlead_bot.db
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

### Option 3: Heroku

1. **Install Heroku CLI**

2. **Create app**
```bash
heroku create innovlead-education-bot
```

3. **Set environment variables**
```bash
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set ANTHROPIC_API_KEY=your_key
heroku config:set BOT_MODE=webhook
heroku config:set WEBHOOK_URL=https://your-app.herokuapp.com
```

4. **Deploy**
```bash
git push heroku main
```

---

## 📊 Monitoring & Maintenance

### Check Logs

**Development:**
```bash
# Logs are shown in console
tail -f logs/bot.log
```

**Production (systemd):**
```bash
sudo journalctl -u innovlead-bot -f
```

**Docker:**
```bash
docker-compose logs -f bot
```

### Monitor Performance

```bash
# Check if bot is running
ps aux | grep "bot.main"

# Check database size
ls -lh innovlead_bot.db

# Monitor resource usage
htop
```

### Backup Database

```bash
# SQLite
cp innovlead_bot.db innovlead_bot_backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump innovlead_bot > backup_$(date +%Y%m%d).sql
```

### Update Bot

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart bot
sudo systemctl restart innovlead-bot
```

---

## 🐛 Troubleshooting

### Bot doesn't respond

**Check:**
1. Is the bot running? `sudo systemctl status innovlead-bot`
2. Is the token correct in `.env`?
3. Check logs: `sudo journalctl -u innovlead-bot -n 50`

### Database errors

```bash
# Reinitialize database (WARNING: Deletes all data!)
rm innovlead_bot.db
python -m database.init_db
```

### AI Tutor not working

**Check:**
1. Is `ENABLE_AI_TUTOR=true` in `.env`?
2. Is AI provider API key valid?
3. Do you have API credits remaining?
4. Check error logs

### Out of memory

**Solution:**
- Upgrade server RAM
- Use PostgreSQL instead of SQLite
- Optimize queries

---

## 📞 Support

**InnovLead Foundation:**
- Email: education@innovlead.org
- Community: @InnovLeadCommunity
- Website: innovlead.org

**Technical Issues:**
- GitHub Issues: [Report Bug](https://github.com/innovlead-foundation/education-bot/issues)
- Email: technical@innovlead.org

---

## 📄 License

MIT License - See LICENSE file

---

**Built with ❤️ by InnovLead Foundation for the people**

🌟 Democratizing AI education, one bot at a time.
