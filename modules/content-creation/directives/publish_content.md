# Directive: Publish Content to Web

## Goal
Publish the generated ELI5 tech topic content and image to the InnovLead platform, making it accessible to the public.

## Inputs
- **Content Data**: Title, ELI5 explanation, tags (from `.tmp/content/{topic_slug}.json`)
- **Image File**: Generated image (from `.tmp/images/{topic_slug}.png`)
- **Topic Metadata**: Source, timestamp, category

## Tools/Scripts
- **Script**: `execution/publish_content.py`
- **Platform**: InnovLead Replit app at https://media-uploader--tommy0110.replit.app/

## Process

### 1. Prepare Content for Publishing
- Format content as HTML or markdown
- Create SEO-friendly title and meta description
- Generate URL slug from topic title (lowercase, hyphens, no special chars)
- Prepare tags for categorization

### 2. Upload Image
- **Option A**: Upload to InnovLead server storage
  - POST image to `/api/upload-image` or similar endpoint
  - Receive public URL for the image
- **Option B**: Use cloud storage (if InnovLead has S3/Cloudinary integration)
- **Option C**: Store locally if InnovLead is self-hosted

### 3. Create Content Entry
- **Method 1**: API endpoint (if InnovLead has one)
  - POST to `/api/content/create` with JSON payload:
    ```json
    {
      "title": "What is Quantum Computing?",
      "slug": "what-is-quantum-computing",
      "content": "ELI5 explanation text...",
      "image_url": "https://...",
      "tags": ["quantum", "computing", "physics"],
      "category": "computer-science",
      "published_at": "2025-12-11T01:00:00Z"
    }
    ```
  
- **Method 2**: Direct file creation (if static site)
  - Create HTML file at `public/library/{slug}.html`
  - Use template with consistent styling
  - Include title, image, explanation, tags

### 4. Update Content Library Index
- Add entry to library index page (`/library` or `/topics`)
- Update sitemap.xml for SEO
- Optionally: update RSS feed if implemented

### 5. Verify Publication
- Check that content is accessible at published URL
- Validate HTML/rendering
- Confirm image loads correctly

## Outputs
- **Published URL**: https://media-uploader--tommy0110.replit.app/topics/{slug}
- **Publication Log**: `.tmp/published/{slug}_log.json` containing:
  ```json
  {
    "topic": "topic name",
    "slug": "url-slug",
    "published_url": "full URL",
    "published_at": "timestamp",
    "status": "success"
  }
  ```

## Edge Cases

### Upload Failure
- **Issue**: Image upload fails or content API returns error
- **Action**: Retry up to 3 times
- **Fallback**: Save content locally and flag for manual review/retry

### Duplicate Content
- **Issue**: Topic already exists (same slug)
- **Action**: 
  - Check if existing content should be updated
  - If yes: replace old version, keep URL same
  - If no: append date to slug (e.g., `topic-name-2025-12`)

### Broken Links
- **Issue**: Published URL doesn't work or returns 404
- **Action**: Verify deployment, check server logs, retry publication

## Publishing Platforms

### Short-term: InnovLead Replit App
- Add new route `/topics` or `/library`
- Create simple page template showing all published topics
- Individual topic pages at `/topics/{slug}`

### Long-term Options
- Ghost CMS integration
- WordPress with custom theme
- Static site generator (11ty, Hugo) deployed to Netlify/Vercel
- Custom React/Next.js app

## SEO Optimization

Each published page should include:
- **Title tag**: "{Topic Title} Explained Simply | InnovLead"
- **Meta description**: First 150 chars of ELI5 explanation
- **Open Graph tags**: For social media sharing
- **Structured data**: Article schema for Google
- **Canonical URL**: Avoid duplicate content issues

## Notes
- Start simple: static HTML files or JSON-based rendering
- Build content library UI later (can be simple list with search)
- Consider using a headless CMS for easier content management eventually
