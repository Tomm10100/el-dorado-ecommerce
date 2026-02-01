# Directive: Generate Topic Image

## Goal
Generate a high-quality, educational visual for a tech topic using the Nano Banana AI image generation service integrated with InnovLead.

## Inputs
- **Image Prompt**: Detailed text prompt describing the desired image (from content generation step)
- **Topic Metadata**: Title, tags, and context

## Tools/Scripts
- **Script**: `execution/generate_topic_image.py`
- **API**: Nano Banana Pro AI (via InnovLead integration)

## Process

### 1. Prepare Image Generation Request
- Use the highly-detailed prompt from content generation
- Set optimal parameters for educational imagery:
  - **Aspect Ratio**: 16:9 (good for web display) or 1:1 (square for social)
  - **Resolution**: High (1024x1024 or 1920x1080)
  - **Style**: Clear, colorful, educational, diagram-style or illustrated
  - **Format**: PNG for quality

### 2. Call Nano Banana API
- Send request to InnovLead's Nano Banana endpoint
- Include prompt and parameters
- Handle API rate limits (wait/retry if needed)
- Timeout: 60 seconds (image generation can be slow)

### 3. Download and Store Image
- Retrieve generated image URL from API response
- Download image file
- Save to `.tmp/images/{topic_slug}.png`
- Also save metadata (prompt used, generation params, timestamp)

### 4. Quality Validation
- Verify image file exists and is valid
- Check file size (should be reasonable, not corrupted)
- Optionally: run basic image analysis (resolution, aspect ratio)

## Outputs
- **Image File**: `.tmp/images/{topic_slug}.png`
- **Metadata File**: `.tmp/images/{topic_slug}_meta.json` containing:
  ```json
  {
    "topic": "topic name",
    "prompt": "full prompt used",
    "generated_at": "timestamp",
    "file_path": "path to image",
    "parameters": {"aspect_ratio": "16:9", "resolution": "1920x1080"}
  }
  ```

## Edge Cases

### API Failure
- **Issue**: Nano Banana API returns error or times out
- **Action**: Retry up to 3 times with exponential backoff (5s, 15s, 30s)
- **Fallback**: If all retries fail, use a placeholder image or skip this topic

### Poor Image Quality
- **Issue**: Generated image doesn't match topic or is low quality
- **Action**: Log the issue, but proceed (quality control can be manual review for now)
- **Future**: Implement automated quality scoring

### Rate Limiting
- **Issue**: Too many requests to Nano Banana API
- **Action**: Implement delay between requests (e.g., 10 seconds)
- **Tracking**: Log API usage to stay within limits

## Notes
- Reuse existing InnovLead Nano Banana integration (check their codebase for API endpoints)
- Keep prompts detailed and specific for best results
- Consider caching: if we regenerate content for same topic, reuse image if prompt unchanged
