# Content Creation Module

**Version**: 1.0.0  
**Status**: Active ✅

## Description

Automated social media content generation for tech education. Creates Instagram/TikTok-ready content with:
- Research from Gemini AI
- ELI5 explanations (100-150 words)
- Professional infographics using Google Imagen4 (Nano Banana)
- Auto-publishing to InnovLead queue

## Usage

### Via Module Manager (Recommended)

```bash
# Run with specific topic
py module_manager.py run content-creation "Quantum Computing"

# Run with topic discovery
py module_manager.py run content-creation

# Check module status
py module_manager.py status content-creation
```

### Direct Execution

```bash
cd modules/content-creation

# Full pipeline
py execution/main_content_pipeline.py "Docker Containers"

# Individual scripts
py execution/discover_trending_topics.py
py execution/research_topic_gemini.py "AI"
py execution/generate_eli5_content.py .tmp/research/ai.json
py execution/generate_image_keiai.py "AI" "Professional infographic..."
```

## Outputs

- **Research**: `.tmp/research/{slug}.json`
- **Content**: `.tmp/content/{slug}.json`
- **Images (temp)**: `.tmp/images/{slug}.png`
- **Final Images**: `outputs/final_pictures/{slug}.png`
  - Also saved to: `Desktop/InnovLead Documents/innovlead automatic content workflow final pictures/`

## Configuration

### Required API Keys (in root `.env`)

```bash
GEMINI_API_KEY=your_key          # Content generation
KEI_AI_API_KEY=your_key          # Image generation (Google Imagen4)
```

### Optional

```bash
PERPLEXITY_API_KEY=your_key      # Premium research (optional)
INNOVLEAD_API_URL=your_url       # Publishing endpoint
```

## Dependencies

- `core.lib.api_client` - HTTP requests
- `core.lib.logger` - Logging
- `core.lib.file_utils` - File operations

## Directives (SOPs)

1. `discover_topics.md` - Find trending tech topics
2. `research_topic.md` - Deep research on topics
3. `generate_content.md` - Create ELI5 posts
4. `generate_image.md` - Create infographics
5. `publish_content.md` - Publish to queue

## Architecture

Follows Antigravity 4-layer protocol:
- **Layer 1**: Directives (SOPs in `directives/`)
- **Layer 2**: Orchestration (AI decision-making)
- **Layer 3**: Context (MCP servers - future)
- **Layer 4**: Execution (Python scripts in `execution/`)

## Cost

**Current**: ~$0-1.50/month (100 posts)
- Gemini: FREE
- Google Imagen4: Via Kei.ai (~$0.05/image)

## Performance

- Topic discovery: ~2s
- Research: ~5-10s
- Content generation: ~5s
- Image generation: ~30-40s
- **Total**: ~50-60s per post

## Status

✅ Fully operational  
✅ Google Imagen4 (Nano Banana) integrated  
⚠️ Publishing endpoint not configured yet
