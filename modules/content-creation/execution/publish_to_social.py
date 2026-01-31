"""
InnovLead Content Engine - Social Media Publishing
Posts generated content and images to social media platforms via InnovLead.

Per directive: directives/publish_content.md (adapted for social media)
"""

import os
import sys
import json

# Fix Unicode encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
import requests
from pathlib import Path
from typing import Dict
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration
PUBLISHED_LOG_DIR = Path(".tmp/published")
INNOVLEAD_API_BASE = os.getenv("INNOVLEAD_API_URL", "https://media-uploader--tommy0110.replit.app")


class SocialMediaPublisher:
    def __init__(self, content_file: str, image_file: str):
        self.content_file = Path(content_file)
        self.image_file = Path(image_file) if image_file else None
        self.content_data = self.load_content()
        self.slug = self.content_data.get("slug", "unknown")
    
    def load_content(self) -> Dict:
        """Load content data from JSON"""
        with open(self.content_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def format_social_post(self) -> str:
        """Format content for social media with hashtags"""
        topic = self.content_data.get("topic", "")
        explanation = self.content_data.get("explanation", "")
        tags = self.content_data.get("tags", [])
        
        # Add hashtags
        hashtags = " ".join([f"#{tag.replace('-', '').replace(' ', '')}" for tag in tags[:5]])
        
        # Format post
        post_text = f"{explanation}\n\n{hashtags}\n\n#InnovLead #TechExplained #ELI5"
        
        return post_text
    
    def post_to_innovlead(self, post_text: str, image_url: str) -> Dict:
        """Post content to InnovLead API for social media distribution"""
        print(f"📱 Posting to social media via InnovLead...")
        
        # Prepare payload for InnovLead
        payload = {
            "title": self.content_data.get("topic"),
            "content": post_text,
            "image_url": image_url,
            "platforms": ["instagram", "tiktok", "facebook"],  # Adjust as needed
            "tags": self.content_data.get("tags", []),
            "category": "tech-education"
        }
        
        try:
            # POST to InnovLead API endpoint for social publishing
            # Adjust endpoint based on your actual InnovLead API structure
            response = requests.post(
                f"{INNOVLEAD_API_BASE}/api/social-publish",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                print(f"  ✅ Posted successfully")
                return {
                    "success": True,
                    "post_id": data.get("id", "unknown"),
                    "platforms": payload["platforms"]
                }
            else:
                print(f"  ⚠️ API returned status {response.status_code}")
                print(f"  Response: {response.text}")
                return {
                    "success": False,
                    "error": f"API returned {response.status_code}"
                }
                
        except Exception as e:
            print(f"  ❌ Publishing error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def save_locally_as_backup(self, post_text: str, image_url: str):
        """Save content locally as backup"""
        output_dir = Path("public/social_posts")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        backup_data = {
            "topic": self.content_data.get("topic"),
            "slug": self.slug,
            "post_text": post_text,
            "image_url": image_url,
            "created_at": datetime.now().isoformat()
        }
        
        backup_file = output_dir / f"{self.slug}.json"
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved backup to {backup_file}")
    
    def log_publication(self, result: Dict):
        """Log publication attempt"""
        PUBLISHED_LOG_DIR.mkdir(parents=True, exist_ok=True)
        
        log_entry = {
            "topic": self.content_data.get("topic"),
            "slug": self.slug,
            "status": "success" if result.get("success") else "failed",
            "platforms": result.get("platforms", []),
            "post_id": result.get("post_id", ""),
            "error": result.get("error", ""),
            "published_at": datetime.now().isoformat()
        }
        
        log_file = PUBLISHED_LOG_DIR / f"{self.slug}_log.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_entry, f, indent=2, ensure_ascii=False)
        
        # Also append to master log
        master_log = PUBLISHED_LOG_DIR / "social_publications.jsonl"
        with open(master_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        print(f"📝 Logged publication")
    
    def publish(self) -> Dict:
        """Main publishing workflow for social media"""
        print(f"\n📱 Publishing to social media: {self.content_data.get('topic')}\n")
        
        try:
            # Format content for social media
            post_text = self.format_social_post()
            
            # Get image URL (should already be uploaded by image generation script)
            image_url = ""
            if self.image_file and self.image_file.exists():
                # In a real scenario, you'd upload to cloud storage and get URL
                # For now, use local path
                image_url = str(self.image_file.absolute())
            
            # Post to InnovLead API
            result = self.post_to_innovlead(post_text, image_url)
            
            # Save backup locally
            self.save_locally_as_backup(post_text, image_url)
            
            # Log publication
            self.log_publication(result)
            
            return result
            
        except Exception as e:
            print(f"❌ Publishing error: {e}")
            error_result = {
                "success": False,
                "error": str(e)
            }
            self.log_publication(error_result)
            return error_result


def main():
    """Run social media publishing"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python publish_to_social.py <content_file> [image_file]")
        print("Example: python publish_to_social.py .tmp/content/quantum-computing.json .tmp/images/quantum-computing.png")
        sys.exit(1)
    
    content_file = sys.argv[1]
    image_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(content_file).exists():
        print(f"❌ Content file not found: {content_file}")
        sys.exit(1)
    
    publisher = SocialMediaPublisher(content_file, image_file)
    result = publisher.publish()
    
    # Display results
    print("\n" + "="*60)
    print(f"📊 SOCIAL MEDIA PUBLISHING RESULT")
    print("="*60 + "\n")
    
    if result.get("success"):
        print(f"✅ Success!")
        print(f"📱 Posted to: {', '.join(result.get('platforms', []))}")
        print(f"🆔 Post ID: {result.get('post_id')}")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
