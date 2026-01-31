# Directive: Run Complete Content Pipeline

## Goal
Orchestrate the full automated content creation workflow from topic discovery to web publication.

## Overview
This is the master workflow that chains together all individual directives:
1. Discover trending topics
2. Select best topic for content creation
3. Research the topic in depth
4. Generate ELI5 content and image prompt
5. Generate the visual
6. Publish to web

## Inputs
- **None** (fully autonomous) OR
- **Specific Topic** (if manually triggered for a particular subject)

## Tools/Scripts
- **Script**: `execution/main_content_pipeline.py`
- **Dependencies**: All other execution scripts

## Process

### 1. Topic Discovery
- Run `discover_trending_topics.py`
- Receive list of trending tech topics with scores
- **Decision Point**: Select top topic OR use manual override

### 2. Topic Selection
- If automated: choose highest-scored topic that hasn't been covered recently
- Check against published content to avoid duplicates
- Validate topic is suitable (relevant, not too broad/narrow)

### 3. Research Phase
- Run `research_topic_deep.py --topic "{selected_topic}"`
- Wait for research completion
- Validate research output has sufficient information
- **Quality Gate**: If research is insufficient, skip this topic and try next one

### 4. Content Generation
- Run `generate_eli5_content.py --research .tmp/research/{topic_slug}.json`
- Wait for content generation
- **Quality Gate**: Validate ELI5 explanation is clear and accurate
  - Check readability score (Flesch-Kincaid grade level < 8)
  - Ensure image prompt is detailed and descriptive

### 5. Image Generation
- Run `generate_topic_image.py --prompt "{image_prompt}" --topic "{topic_slug}"`
- Wait for image generation (can take 30-60 seconds)
- **Quality Gate**: Verify image file was created successfully

### 6. Publication
- Run `publish_content.py --content .tmp/content/{topic_slug}.json --image .tmp/images/{topic_slug}.png`
- Wait for publication
- **Quality Gate**: Verify published URL is accessible

### 7. Cleanup and Logging
- Log successful publication to `.tmp/pipeline_log.json`
- Archive intermediate files (optional: delete or keep for debugging)
- Update "recently covered topics" list to avoid duplicates

## Outputs
- **Published Content**: Live on InnovLead platform
- **Pipeline Log**: `.tmp/pipeline_log.json` with entry:
  ```json
  {
    "run_id": "unique_id",
    "timestamp": "2025-12-11T01:00:00Z",
    "topic": "selected topic",
    "status": "success",
    "published_url": "https://...",
    "steps_completed": ["discover", "research", "generate", "image", "publish"],
    "duration_seconds": 180
  }
  ```

## Error Handling Strategy

### Soft Failures (Retry)
- API timeouts → retry with backoff
- Temporary network issues → retry
- Rate limiting → wait and retry

### Hard Failures (Skip)
- Invalid topic (research failed) → skip to next topic
- Content quality too low → skip and try next
- Image generation fails after retries → skip (fallback: use placeholder or text-only)

### Critical Failures (Alert)
- All API keys invalid → stop and alert user
- No topics found → alert (may need to adjust discovery sources)
- Publishing completely broken → stop and alert

## Scheduling

### Manual Execution
```bash
python execution/main_content_pipeline.py
```

### Automated Scheduling
- **Windows**: Task Scheduler
  - Trigger: Daily at 9 AM
  - Action: Run `python main_content_pipeline.py`
- **Linux/Mac**: Cron job
  ```cron
  0 9 * * * cd /path/to/Antigravity && python execution/main_content_pipeline.py
  ```

### Frequency Recommendations
- **Daily**: 1 new topic per day (manageable, consistent growth)
- **Weekly**: 2-3 topics per week (less aggressive, higher quality control)
- **On-demand**: Run manually when needed

## Monitoring

### Success Metrics
- **Completion Rate**: % of runs that successfully publish content
- **Quality Score**: User engagement, bounce rate on published pages
- **Cost**: API usage and costs per piece of content

### Alerts
- Email/SMS notification on critical failures
- Weekly summary report of published content
- Monthly analytics on content library growth

## Continuous Improvement

### Self-Annealing
When errors occur:
1. **Analyze** the error message and context
2. **Fix** the underlying script or directive
3. **Test** the fix
4. **Update** this directive with learnings

### Examples of Learnings to Document
- "Nano Banana API has 50 req/day limit → space out runs by 1 hour"
- "Research quality is best from Wikipedia + HackerNews combinations"
- "Avoid topics with <3 quality sources, they produce poor ELI5 content"

## Quality Control Gates

Before proceeding to next step, validate:
- [ ] Topic is tech-related and educational
- [ ] Research has at least 3 quality sources
- [ ] ELI5 explanation is < 300 words and grade level < 8
- [ ] Image prompt is > 50 words and descriptive
- [ ] Image file is valid and > 100KB
- [ ] Published URL returns 200 status

If any gate fails, log the issue and either retry or skip.

## Notes
- Start with manual runs to test the full pipeline
- Once stable, automate with scheduler
- Review published content weekly for quality
- Gather user feedback to improve prompts and selection criteria
