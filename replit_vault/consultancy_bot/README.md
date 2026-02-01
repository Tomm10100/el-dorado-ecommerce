# ConsultancyBot Package

**Dynamic, Reusable Consultancy Automation for Any Industry**

This package transforms the hardcoded "Jewelry Consultancy" scripts into a powerful, industry-agnostic consultancy automation system.

## 🎯 What It Does

ConsultancyBot automates the complete consultancy workflow:

1. **Client Research** - Analyze company website, tech stack, team
2. **Competitor Research** - Find and analyze real competitors in any industry
3. **Funding Research** - Identify grants, tax credits, and incentives
4. **Strategy Generation** - AI-powered opportunity identification
5. **Proposal Generation** - Professional, template-based proposals

## 🏗️ Architecture

```
replit_vault/consultancy_bot/
├── __init__.py                  # Package initialization
├── bot.py                       # Main orchestrator (ConsultancyBot class)
├── competitor_research.py       # Dynamic competitor analysis
├── proposal_generator.py        # Template-based proposal generation
├── templates/
│   ├── executive_summary.md     # Executive summary template (Jinja2)
│   ├── technical_roadmap.md     # Technical roadmap template (optional)
│   └── financial_model.md       # Financial model template (optional)
└── README.md                    # This file
```

## 🚀 Quick Start

### Basic Usage

```python
from replit_vault.consultancy_bot import ConsultancyBot

# Initialize the bot
bot = ConsultancyBot(verbose=True)

# Run the complete workflow
results = bot.run(
    company_url="https://example.com",
    industry="SaaS CRM",
    company_name="TechCorp",
    location="Canada",
    num_competitors=5
)

# Access results
print(f"Proposal: {results['files']['proposal']}")
print(f"Strategy: {results['files']['strategy']}")
print(f"Competitors: {results['files']['competitors']}")
```

### Command Line Usage

```bash
# Run complete consultancy workflow
python bot.py <company_url> <industry> [company_name] [location]

# Example
python bot.py https://example.com "SaaS CRM" "TechCorp" "USA"
```

### Individual Module Usage

#### Competitor Research Only

```python
from replit_vault.consultancy_bot import CompetitorResearcher

researcher = CompetitorResearcher()
results = researcher.research_competitors(
    industry="jewelry e-commerce",
    location="Canada",
    num_competitors=5
)

# Save results
researcher.save_research(results, "ClientName")
```

```bash
# Command line
python competitor_research.py "SaaS CRM" "USA" "TechCorp"
```

#### Proposal Generation Only

```python
from replit_vault.consultancy_bot import ProposalGenerator

generator = ProposalGenerator()
proposal = generator.generate_executive_summary(
    company_name="TechCorp",
    industry="SaaS",
    strategy_data=strategy_json,
    competitor_data=competitor_json,
    funding_data=funding_json
)

# Save proposal
generator.save_proposal(proposal, "TechCorp", "executive_summary")
```

## 🔧 Components

### 1. ConsultancyBot (`bot.py`)

Main orchestrator that runs the complete workflow.

**Key Methods:**
- `run()` - Execute complete consultancy workflow
- `_research_client()` - Research client company
- `_save_funding_research()` - Save funding data
- `_save_strategy()` - Save strategy data

### 2. CompetitorResearcher (`competitor_research.py`)

Dynamic competitor research using Brave Search API.

**Key Methods:**
- `research_competitors()` - Find and analyze competitors
- `_analyze_competitor()` - Detailed competitor analysis
- `_generate_market_insights()` - Extract market intelligence
- `_identify_gaps()` - Find strategic opportunities

**Features:**
- Real-time web search for competitors
- AI-powered competitive intelligence
- Market trend analysis
- Strategic gap identification

### 3. ProposalGenerator (`proposal_generator.py`)

Template-based proposal generation using Jinja2.

**Key Methods:**
- `generate_executive_summary()` - Create executive summary
- `generate_technical_roadmap()` - Create technical plan
- `generate_financial_model()` - Create financial projections
- `save_proposal()` - Save to file

**Features:**
- Jinja2 templating for flexibility
- Custom filters (currency, date, percentage)
- Multiple proposal types
- Graceful fallbacks

### 4. Templates (`templates/`)

Jinja2 templates for professional proposals.

**Executive Summary Template:**
- Market intelligence section
- Competitive analysis
- Strategic opportunities
- InnovLead solution overview
- Implementation roadmap
- Investment summary

## 📊 Data Flow

```
Input: company_url, industry, location
    ↓
[Client Research]
    ↓
[Competitor Research] → competitor_data.json
    ↓
[Funding Research] → funding_data.json
    ↓
[Strategy Generation] → strategy_data.json
    ↓
[Proposal Generation] → executive_summary.md
    ↓
Output: Complete proposal suite
```

## 🎨 Template Variables

Templates have access to:

```python
{
    'company_name': str,
    'industry': str,
    'date': datetime,
    'strategy': {
        'executive_summary': str,
        'analysis_matrix': [dict],
        'opportunities': [dict],
        'draft_email': str
    },
    'competitors': {
        'industry': str,
        'location': str,
        'competitors': [dict],
        'market_insights': dict,
        'competitive_gaps': [dict]
    },
    'funding': {
        'opportunities': [dict],
        'tax_incentives': [dict],
        'quick_wins': [dict]
    },
    'innovlead': {
        'contact': dict,
        'credentials': [str]
    }
}
```

## 🔑 Requirements

### Python Packages
```
jinja2
requests (for Gemini API)
```

### Environment Variables
```
GEMINI_API_KEY=your_api_key
BRAVE_API_KEY=your_brave_api_key (optional)
```

### Dependencies
- `modules.mcp_integrations.execution.brave_search_connector` (for search)
- `modules.client-automation.execution.research_funding` (funding research)
- `modules.client-automation.execution.generate_strategy` (strategy generation)
- `core.lib.api_client` (Gemini API)

## 📝 Examples

### Example 1: SaaS Company

```python
from replit_vault.consultancy_bot import run_consultancy

results = run_consultancy(
    company_url="https://saas-startup.com",
    industry="SaaS CRM",
    company_name="CRMpro",
    location="USA"
)
```

### Example 2: E-commerce Business

```python
bot = ConsultancyBot(verbose=True)
results = bot.run(
    company_url="https://jewelry-store.com",
    industry="jewelry e-commerce",
    company_name="Silver Haven",
    location="Canada"
)
```

### Example 3: Restaurant Tech

```python
results = run_consultancy(
    company_url="https://restaurant-tech.com",
    industry="restaurant technology",
    company_name="FoodTech Inc",
    location="Canada",
    num_competitors=3
)
```

## 🎯 Key Improvements Over Hardcoded Version

| Aspect | Old (Hardcoded) | New (Dynamic) |
|--------|----------------|---------------|
| **Industry** | Jewelry only | Any industry |
| **Competitor Data** | Fake/hardcoded | Real web search |
| **Proposal** | Hardcoded strings | Jinja2 templates |
| **Reusability** | Single-use | Infinitely reusable |
| **Maintenance** | Edit code each time | Edit templates |
| **Scalability** | Manual per client | Automated workflow |

## 🔮 Future Enhancements

- [ ] Additional proposal templates (technical, financial)
- [ ] HTML/PDF output generation
- [ ] Multi-language support
- [ ] Custom branding injection
- [ ] Email automation integration
- [ ] CRM integration
- [ ] Web scraping for deeper competitor analysis
- [ ] Social media sentiment analysis
- [ ] Industry-specific templates

## 🤝 Integration

### With Replit Vault

```python
# In replit_vault/server.py
from replit_vault.consultancy_bot import ConsultancyBot

@app.route('/api/consultancy/run', methods=['POST'])
def run_consultancy_api():
    data = request.json
    bot = ConsultancyBot()
    results = bot.run(
        company_url=data['url'],
        industry=data['industry'],
        company_name=data.get('company_name'),
        location=data.get('location', 'Canada')
    )
    return jsonify(results)
```

### With Existing Modules

The ConsultancyBot seamlessly integrates with existing modules:
- `modules.client-automation` - Research and strategy
- `modules.mcp_integrations` - Brave Search API
- `core.lib.api_client` - Gemini AI

## 📄 License

Proprietary - InnovLead Canada Inc.

## 👤 Author

William Meléndez Salas, MBA  
InnovLead Canada Inc.

---

**"The consultancy is the moat. The automation is the product. The vault is the asset."**
