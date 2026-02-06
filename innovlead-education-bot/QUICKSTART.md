# ⚡ Quick Start Guide - InnovLead Education Bot

Get your bot running in 5 minutes!

---

## 🚀 Super Fast Setup

### 1. Install Python Dependencies
```bash
cd innovlead-education-bot
pip install -r requirements.txt
```

### 2. Get Your Bot Token
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow instructions
3. Copy your bot token

### 3. Get API Key
- **Anthropic Claude**: [console.anthropic.com](https://console.anthropic.com) (Recommended)
- **OR OpenAI**: [platform.openai.com](https://platform.openai.com)

### 4. Configure Environment
```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Edit `.env`:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
ANTHROPIC_API_KEY=your_api_key_here
```

### 5. Initialize Database
```bash
python -m database.init_db
```

### 6. Run the Bot!
```bash
python -m bot.main
```

### 7. Test on Telegram
Search for your bot and send `/start`

---

## 🎯 Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome & registration |
| `/aprender` | Access learning modules |
| `/privacidad` | Quick PIPEDA privacy tips |
| `/progreso` | View your progress |
| `/ayuda` | Help & support |

---

## 📚 What's Included

### 3 Educational Modules

**🤖 AI Ethics & Responsible AI** (5 lessons)
- AI Fundamentals
- Recognizing Bias
- Generative AI Ethics
- AI in Public Services
- Building Responsible AI

**🔒 Privacy in Canada (PIPEDA)** (6 lessons)
- Introduction to PIPEDA
- Data Protection Rights
- Consent Management
- Data Breach Response
- Privacy for NGOs
- Exercising Your Rights

**⚡ Social Automation** (4 lessons)
- Automation Basics
- Introduction to n8n
- Workflow Design
- Maximum Productivity, Zero Budget

---

## 🛠️ Troubleshooting

**Bot doesn't start?**
- Check your `.env` file has correct tokens
- Ensure Python 3.9+ is installed
- Run `pip install -r requirements.txt` again

**Database error?**
```bash
rm innovlead_bot.db
python -m database.init_db
```

**AI Tutor not working?**
- Verify API key in `.env`
- Check you have API credits
- Set `ENABLE_AI_TUTOR=true`

---

## 📖 Full Documentation

- [README.md](README.md) - Complete overview
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Production deployment
- [LICENSE](LICENSE) - MIT License

---

## 🤝 Support

**InnovLead Foundation:**
- Email: education@innovlead.org
- Community: @InnovLeadCommunity
- Website: innovlead.org

---

**Built with ❤️ for InnovLead Foundation**

🌟 Democratizing AI education, one bot at a time.
