"""
InnovLead Content Engine - Content Publishing
Publishes generated content and images to the InnovLead platform.

Per directive: directives/publish_content.md
"""

import os
import json
import requests
from pathlib import Path
from typing import Dict
from datetime import datetime
import shutil


# Configuration
PUBLISHED_LOG_DIR = Path(".tmp/published")
INNOVLEAD_API_BASE = os.getenv("INNOVLEAD_API_URL", "https://media-uploader--tommy0110.replit.app")
PUBLISH_METHOD = os.getenv("PUBLISH_METHOD", "static")  # Options: 'api', 'static', 'manual'


class ContentPublisher:
    def __init__(self, content_file: str, image_file: str):
        self.content_file = Path(content_file)
        self.image_file = Path(image_file) if image_file else None
        self.content_data = self.load_content()
        self.slug = self.content_data.get("slug", "unknown")
    
    def load_content(self) -> Dict:
        """Load content data from JSON"""
        with open(self.content_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def upload_image(self) -> str:
        """Upload image and return public URL"""
        print(f"📤 Uploading image...")
        
        if not self.image_file or not self.image_file.exists():
            print("  ⚠️ No image file provided")
            return ""
        
        # TODO: Implement actual image upload based on InnovLead's backend
        # Options:
        # 1. POST to InnovLead API endpoint
        # 2. Upload to cloud storage (S3, Cloudinary, etc.)
        # 3. Copy to public directory if static site
        
        # PLACEHOLDER: Return local path as URL
        print("  ⚠️ Using placeholder image upload")
        return f"/images/{self.slug}.png"
    
    def generate_html_page(self, image_url: str) -> str:
        """Generate HTML page for the content"""
        topic = self.content_data.get("topic", "Untitled")
        explanation = self.content_data.get("explanation", "")
        tags = self.content_data.get("tags", [])
        sources = self.content_data.get("sources", [])
        
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic} Explained Simply | InnovLead</title>
    <meta name="description" content="{explanation[:150]}...">
    
    <!-- Open Graph / Social Media -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{topic} Explained Simply">
    <meta property="og:description" content="{explanation[:150]}...">
    <meta property="og:image" content="{image_url}">
    
    <!-- Keywords -->
    <meta name="keywords" content="{', '.join(tags)}">
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 20px;
            text-align: center;
            margin-bottom: 40px;
        }}
        
        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .content-card {{
            background: white;
            border-radius: 12px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .featured-image {{
            width: 100%;
            border-radius: 8px;
            margin: 30px 0;
        }}
        
        .explanation {{
            font-size: 1.1em;
            line-height: 1.8;
            margin: 20px 0;
        }}
        
        .tags {{
            margin-top: 30px;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .tag {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        
        .sources {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #eee;
        }}
        
        .sources h3 {{
            margin-bottom: 15px;
            color: #667eea;
        }}
        
        .sources a {{
            color: #667eea;
            text-decoration: none;
        }}
        
        .sources a:hover {{
            text-decoration: underline;
        }}
        
        footer {{
            text-align: center;
            padding: 40px 20px;
            color: #666;
        }}
    </style>
</head>
<body>
    <header>
        <h1>{topic}</h1>
        <p class="subtitle">Explained Simply</p>
    </header>
    
    <div class="container">
        <div class="content-card">
            {f'<img src="{image_url}" alt="{topic}" class="featured-image">' if image_url else ''}
            
            <div class="explanation">
                {explanation.replace(chr(10), '<br><br>')}
            </div>
            
            <div class="tags">
                {chr(10).join(f'<span class="tag">{tag}</span>' for tag in tags)}
            </div>
            
            {f'''<div class="sources">
                <h3>Learn More:</h3>
                <ul>
                    {chr(10).join(f'<li><a href="{source}" target="_blank">{source}</a></li>' for source in sources if source)}
                </ul>
            </div>''' if sources else ''}
        </div>
    </div>
    
    <footer>
        <p>&copy; 2025 InnovLead | Making Technology Simple</p>
    </footer>
</body>
</html>"""
        
        return html_template
    
    def publish_static(self, html_content: str) -> str:
        """Publish as static HTML file"""
        print(f"📄 Publishing as static HTML...")
        
        # Create output directory
        output_dir = Path("public/topics")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save HTML file
        html_file = output_dir / f"{self.slug}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Copy image if exists
        if self.image_file and self.image_file.exists():
            images_dir = Path("public/images")
            images_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy(self.image_file, images_dir / f"{self.slug}.png")
        
        # Construct URL (adjust based on deployment)
        published_url = f"{INNOVLEAD_API_BASE}/topics/{self.slug}.html"
        
        print(f"  ✅ Published to {html_file}")
        return published_url
    
    def publish_via_api(self, image_url: str) -> str:
        """Publish via InnovLead API endpoint"""
        print(f"🌐 Publishing via API...")
        
        # TODO: Implement actual API publishing
        # Example:
        # payload = {
        #     "title": self.content_data.get("topic"),
        #     "slug": self.slug,
        #     "content": self.content_data.get("explanation"),
        #     "image_url": image_url,
        #     "tags": self.content_data.get("tags"),
        #     "sources": self.content_data.get("sources")
        # }
        # 
        # response = requests.post(
        #     f"{INNOVLEAD_API_BASE}/api/content/create",
        #     json=payload,
        #     timeout=10
        # )
        
        print("  ⚠️ API publishing not yet implemented")
        return f"{INNOVLEAD_API_BASE}/topics/{self.slug}"
    
    def log_publication(self, published_url: str):
        """Log successful publication"""
        PUBLISHED_LOG_DIR.mkdir(parents=True, exist_ok=True)
        
        log_entry = {
            "topic": self.content_data.get("topic"),
            "slug": self.slug,
            "published_url": published_url,
            "published_at": datetime.now().isoformat(),
            "status": "success"
        }
        
        log_file = PUBLISHED_LOG_DIR / f"{self.slug}_log.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_entry, f, indent=2, ensure_ascii=False)
        
        # Also append to master log
        master_log = PUBLISHED_LOG_DIR / "publications.jsonl"
        with open(master_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        print(f"📝 Logged publication")
    
    def publish(self) -> Dict:
        """Main publishing workflow"""
        print(f"\n🚀 Publishing content: {self.content_data.get('topic')}\n")
        
        try:
            # Upload image
            image_url = self.upload_image()
            
            # Generate HTML
            html_content = self.generate_html_page(image_url)
            
            # Publish based on method
            if PUBLISH_METHOD == "api":
                published_url = self.publish_via_api(image_url)
            else:  # static or manual
                published_url = self.publish_static(html_content)
            
            # Log publication
            self.log_publication(published_url)
            
            return {
                "success": True,
                "published_url": published_url,
                "slug": self.slug
            }
            
        except Exception as e:
            print(f"❌ Publishing error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


def main():
    """Run content publishing"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python publish_content.py <content_file> [image_file]")
        print("Example: python publish_content.py .tmp/content/quantum-computing.json .tmp/images/quantum-computing.png")
        sys.exit(1)
    
    content_file = sys.argv[1]
    image_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(content_file).exists():
        print(f"❌ Content file not found: {content_file}")
        sys.exit(1)
    
    publisher = ContentPublisher(content_file, image_file)
    result = publisher.publish()
    
    # Display results
    print("\n" + "="*60)
    print(f"📊 PUBLISHING RESULT")
    print("="*60 + "\n")
    
    if result.get("success"):
        print(f"✅ Success!")
        print(f"🌐 Published URL: {result['published_url']}")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
