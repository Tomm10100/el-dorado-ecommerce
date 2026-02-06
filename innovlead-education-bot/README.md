# 🎓 InnovLead Universal AI Education Bot

**Democratizing AI & Privacy Education for Vulnerable Communities**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

---

## 📖 About InnovLead Foundation

**InnovLead Foundation** is a Canadian nonprofit organization (in registration as Registered Charity) dedicated to democratizing access to Artificial Intelligence education and privacy compliance (PIPEDA) for vulnerable communities and NGOs across Canada.

**Leadership:**
- **Tommy Fernandez** - Executive Director
- **William Melendez** - Technical Chair

**Mission:** Provide free, accessible AI and privacy education to empower communities without resources.

---

## 🤖 What is This Bot?

The **InnovLead Universal AI Education Bot** is a Telegram-based learning platform that serves as:

✅ **Educational Platform**: Free AI ethics, PIPEDA, and automation training  
✅ **CRA Compliance Tool**: Demonstrates tangible educational activity for charity status  
✅ **Impact Tracker**: Logs user progress for social impact reporting  
✅ **Non-Commercial**: Strictly educational, no consulting services offered  

---

## 🎯 Features

### Educational Modules
1. **AI Ethics & Responsible AI** (5 lessons)
   - Understanding AI fundamentals
   - Recognizing AI bias
   - Ethical use of generative AI
   - AI in public services
   - Building responsible AI systems

2. **Privacy in Canada (PIPEDA Focus)** (6 lessons)
   - Introduction to PIPEDA
   - Data protection rights
   - Consent management
   - Data breach response
   - Privacy for NGOs
   - Individual rights under PIPEDA

3. **Social Automation (Low-Code Tools)** (4 lessons)
   - Automation basics
   - Introduction to n8n
   - Workflow design for nonprofits
   - Productivity without budget

### Bot Commands
- `/start` - Welcome & user registration
- `/aprender` - Access educational modules
- `/privacidad` - Quick PIPEDA tips
- `/progreso` - View your learning progress
- `/ayuda` - Help & community resources

### AI Tutor Integration
- Powered by Anthropic Claude
- Educational, empowering tone
- Non-commercial response filtering
- Context-aware learning assistance

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Telegram account
- Anthropic API key (Claude)
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/innovlead-foundation/education-bot.git
cd innovlead-education-bot
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials
# TELEGRAM_BOT_TOKEN=your_token_here
# ANTHROPIC_API_KEY=your_api_key_here
```

5. **Initialize database**
```bash
python -m database.init_db
```

6. **Run the bot**
```bash
python -m bot.main
```

---

## 📁 Project Structure

```
innovlead-education-bot/
├── bot/                      # Bot core & handlers
│   ├── main.py              # Entry point
│   ├── handlers/            # Command handlers
│   └── middleware/          # User tracking, rate limiting
├── modules/                 # Educational content
│   ├── module_1_ai_ethics/
│   ├── module_2_privacy_canada/
│   └── module_3_automation/
├── ai/                      # AI tutor engine
├── database/                # Database models & connection
├── reporting/               # CRA impact reports
├── config/                  # Configuration
├── templates/               # Message templates
└── docs/                    # Documentation
```

---

## 🔒 Privacy & PIPEDA Compliance

This bot is designed with privacy-first principles:

- ✅ User consent required for data processing
- ✅ Minimal data collection (Telegram ID, username, progress)
- ✅ Data retention policies (365 days active, then anonymized)
- ✅ No personal information shared with third parties
- ✅ Transparent data usage (education & CRA reporting only)

See [PRIVACY_POLICY.md](docs/PRIVACY_POLICY.md) for details.

---

## 📊 CRA Compliance & Impact Reporting

The bot automatically tracks:
- Number of unique users educated
- Module completion rates
- Geographic distribution
- Lesson engagement metrics

Generate reports for CRA T3010 filing:
```bash
python -m reporting.cra_impact_report --period quarterly
```

---

## 🤝 Contributing

We welcome contributions! InnovLead Foundation is committed to open-source, community-driven development.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Why MIT?** As a nonprofit, we believe education should be freely accessible, modifiable, and shareable.

---

## 🌟 Acknowledgments

- **Anthropic** for Claude AI API
- **python-telegram-bot** community
- All contributors to open-source education

---

## 📞 Contact

**InnovLead Foundation**  
- Website: [innovlead.org](https://innovlead.org)
- Email: education@innovlead.org
- Telegram Community: [@InnovLeadCommunity](https://t.me/innovleadcommunity)

---

## 🚨 Important Legal Notice

**This bot is for educational purposes only.**  
InnovLead Foundation is a nonprofit organization and does NOT offer commercial consulting services. If you need professional AI/privacy consulting, please refer to qualified service providers in your area.

---

**Built with ❤️ by InnovLead Foundation for the people**
