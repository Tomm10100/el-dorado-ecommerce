# 🚀 InnovLead Content Automation Engine

> **Automated social media content creation for tech education**  
> ELI5 explanations • Professional infographics • Zero cost

[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)]()
[![Cost](https://img.shields.io/badge/monthly%20cost-$0-success)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

---

## 🎯 What It Does

Automatically creates **Instagram/TikTok-ready tech education content**:
1. 🔍 **Discovers** trending tech topics (AI, blockchain, quantum, etc.)
2. 📚 **Researches** with Gemini AI (comprehensive, accurate)
3. ✍️ **Generates** 100-150 word ELI5 social media posts
4. 🎨 **Creates** professional infographic images with Ideogram
5. 📱 **Publishes** to queue for social media posting

**Result**: Daily viral-worthy content explaining complex tech to anyone! 🌟

---

## 💰 Cost Breakdown

| Service | Purpose | Free Tier | Cost |
|---------|---------|-----------|------|
| **Gemini 2.0** | Research + Content | 60 req/min | **$0** |
| **Ideogram** | Images | 100/month | **$0** |
| **InnovLead** | Publishing | Unlimited | **$0** |
| **TOTAL** | Full automation | 100 posts/month | **$0** ✨ |

---

## 🏗️ Architecture

### 3-Layer System Design

```
┌─────────────────────────────────────────────┐
│  Layer 1: DIRECTIVES (What to do)          │
│  ├── discover_topics.md                    │
│  ├── research_topic.md                     │
│  ├── generate_eli5_content.md              │
│  ├── generate_topic_image.md               │
│  └── publish_content.md                    │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Layer 2: ORCHESTRATION (Decision making)  │
│  └── AI Agent (you!) reads & routes        │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Layer 3: EXECUTION (Doing the work)       │
│  ├── discover_trending_topics.py           │
│  ├── research_topic_gemini.py              │
│  ├── generate_eli5_content.py              │
│  ├── generate_image_ideogram.py            │
│  ├── publish_to_social.py                  │
│  └── main_content_pipeline.py              │
└─────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Gemini API key (free at https://makersuite.google.com/app/apikey)
- Ideogram API key (free at https://ideogram.ai/api-keys)

### Installation

```bash
# Clone or navigate to project
cd Antigravity

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env and add your keys
```

### First Run

```bash
# Run full pipeline with a specific topic
python execution/main_content_pipeline.py "Quantum Computing"

# Or let it discover topics automatically
python execution/main_content_pipeline.py
```

**Output**:
- Research → `.tmp/research/quantum-computing.json`
- Content → `.tmp/content/quantum-computing.json`
- Image → `.tmp/images/quantum-computing.png`
- Log → `.tmp/published/quantum-computing_log.json`

---

## 📖 Usage

### Individual Scripts

```bash
# 1. Discover trending topics
python execution/discover_trending_topics.py

# 2. Research a topic
python execution/research_topic_gemini.py "Neural Networks"

# 3. Generate social media content
python execution/generate_eli5_content.py .tmp/research/neural-networks.json

# 4. Generate image
python execution/generate_image_ideogram.py "Neural Networks" "Colorful infographic..."

# 5. Publish to queue
python execution/publish_to_social.py .tmp/content/neural-networks.json .tmp/images/neural-networks.png
```

### Automated Daily Posts

**Option 1: Manual Daily Run**
```bash
python execution/main_content_pipeline.py
```

**Option 2: Windows Task Scheduler**
- Task name: InnovLead Daily Content
- Trigger: Daily at 9:00 AM
- Program: `python`
- Arguments: `execution/main_content_pipeline.py`
- Start in: `C:\Users\...\Antigravity`

**Option 3: n8n Automation** (see `publishing_endpoint_guide.md`)

---

## ⚙️ Configuration

### Environment Variables (`.env`)

```bash
# Research (optional - Gemini is default)
PERPLEXITY_API_KEY=         # Optional premium research

# Content Generation (required)
GEMINI_API_KEY=your_key     # Get at makersuite.google.com

# Image Generation (required)
IDEOGRAM_API_KEY=your_key   # Get at ideogram.ai/api-keys

# Publishing
INNOVLEAD_API_URL=https://media-uploader--tommy0110.replit.app
PUBLISH_METHOD=social_media

# Optional: n8n webhook for auto-publishing
N8N_SOCIAL_WEBHOOK=your_webhook_url
```

---

## 📊 Example Output

### Generated Social Post
```
Ever wondered how quantum computers work? 

Think of it like a coin spinning in the air - it's both heads 
and tails at the same time! That's superposition. Quantum 
computers use qubits instead of regular bits, letting them 
explore many solutions simultaneously.

Why it matters: They'll revolutionize drug discovery, break 
current encryption, and solve problems impossible for regular 
computers. We're at the iPhone 1 stage of quantum computing!

#QuantumComputing #TechExplained #ELI5 #Innovation
```

### Generated Image
Professional infographic with:
- Vibrant purple/blue gradients
- Clean diagram showing qubit vs bit
- Spinning coin metaphor visualization
- "QUANTUM COMPUTING EXPLAINED" text overlay
- 1024x1024 perfect for Instagram/TikTok

---

## 🛠️ Project Structure

```
Antigravity/
├── directives/              # SOPs (instructions)
│   ├── discover_topics.md
│   ├── research_topic.md
│   ├── generate_eli5_content.md
│   ├── generate_topic_image.md
│   ├── publish_content.md
│   └── run_content_pipeline.md
│
├── execution/               # Python scripts
│   ├── discover_trending_topics.py
│   ├── research_topic_gemini.py
│   ├── research_topic_perplexity.py (optional)
│   ├── generate_eli5_content.py
│   ├── generate_image_ideogram.py
│   ├── publish_to_social.py
│   └── main_content_pipeline.py
│
├── .tmp/                    # Generated content
│   ├── trending_topics.json
│   ├── research/{slug}.json
│   ├── content/{slug}.json
│   ├── images/{slug}.png
│   └── published/{slug}_log.json
│
├── .env                     # API keys (gitignored)
├── .env.example             # Template
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

---

## 🧪 Testing

```bash
# Test topic discovery
python execution/discover_trending_topics.py

# Test research
python execution/research_topic_gemini.py "Blockchain"

# Test full pipeline
python execution/main_content_pipeline.py "Docker Containers"

# Verify queue endpoint (if Replit is running)
curl https://media-uploader--tommy0110.replit.app/api/social-queue
```

---

## 📈 Scaling

### Free Tier (Current)
- 100 posts/month
- $0/month
- Perfect for daily posting

### When You Grow
- **200-400 posts**: Ideogram Basic ($8/mo)
- **Better research**: Add Perplexity ($10/mo)
- **1000+ posts**: Ideogram Plus ($16/mo)

**Even at scale: $16-26/month** vs typical $50-100/month for similar quality!

---

## 🐛 Troubleshooting

### Common Issues

**"GEMINI_API_KEY not set"**
→ Check `.env` file has the key (no quotes)

**Empty content generated**
→ Curated fallback will activate. Add more topics to knowledge base.

**Image generation fails**
→ Verify Ideogram API key is correct. Check quota (100/month free).

**Publishing fails**
→ Ensure Replit endpoint is running and `INNOVLEAD_API_URL` is set.

### Logs

Check `.tmp/pipeline_log.jsonl` for execution history and errors.

---

## 🤝 Contributing

This is a personal automation project, but feel free to:
- Fork and adapt for your own use
- Submit issues if you find bugs
- Share improvements to directives or prompts

---

## 📜 License

MIT License - Use freely for your content automation!

---

## 🙏 Acknowledgments

Built with:
- **Google Gemini** - AI research and content generation
- **Ideogram** - Social media image generation
- **InnovLead** - Publishing platform
- **n8n** - Workflow automation (optional)

---

## 📞 Support

Questions? Check the artifacts folder for detailed guides:
- `implementation_plan.md` - Full technical plan
- `walkthrough.md` - Setup walkthrough
- `deployment_checklist.md` - Launch checklist
- `publishing_endpoint_guide.md` - Endpoint setup

---

**Built to make tech education accessible to everyone! 🚀**

*Last updated: December 2025*
