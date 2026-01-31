"""
InnovLead Content Engine - Image Generation
Generates educational images using Kei.ai API.

Per directive: directives/generate_topic_image.md
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
import time


# Configuration
OUTPUT_DIR = Path(".tmp/images")

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

INNOVLEAD_API_BASE = os.getenv("INNOVLEAD_API_URL", "https://media-uploader--tommy0110.replit.app")
KEI_AI_API_KEY = os.getenv("KEI_AI_API_KEY", "")
KEI_AI_API_URL = "https://api.kei.ai/v1/images/generations"


class ImageGenerator:
    def __init__(self, topic: str, prompt: str):
        self.topic = topic
        self.prompt = prompt
        self.topic_slug = self.create_slug(topic)
        self.max_retries = 3
        self.retry_delays = [5, 15, 30]  # Exponential backoff
    
    def create_slug(self, text: str) -> str:
        """Create URL-friendly slug"""
        slug = text.lower()
        slug = ''.join(c if c.isalnum() or c == ' ' else '' for c in slug)
        slug = '-'.join(slug.split())
        return slug[:50]
    
    def generate_image(self) -> Dict:
        """Generate image using Nano Banana API"""
        print(f"🎨 Generating image for '{self.topic}'...")
        
        # Prepare request payload
        payload = {
            "prompt": self.prompt,
            "aspect_ratio": "16:9",
            "resolution": "1920x1080",
            "output_format": "png",
            "style": "educational, diagram, colorful, clear"
        }
        
        for attempt in range(self.max_retries):
            try:
                print(f"  Attempt {attempt + 1}/{self.max_retries}...")
                
                # Call Kei.ai API for image generation
                response = requests.post(
                    KEI_AI_API_URL,
                    json={
                        "prompt": self.prompt,
                        "aspect_ratio": "1:1",  # Square for social media
                        "n": 1
                    },
                    headers={
                        "Authorization": f"Bearer {KEI_AI_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    image_url = data.get("data", [{}])[0].get("url", "")
                    
                    if image_url:
                        print(f"  ✅ Image generated successfully")
                        return {
                            "success": True,
                            "image_url": image_url,
                            "prompt_used": self.prompt,
                            "parameters": payload
                        }
                    else:
                        print("  ❌ No image URL in response")
                        return {"success": False, "error": "No image URL returned"}
                else:
                    print(f"  ❌ API error: {response.status_code} - {response.text}")
                    return {"success": False, "error": f"API returned {response.status_code}"}
                
                
            except requests.exceptions.Timeout:
                print(f"  ⏱️ Request timeout on attempt {attempt + 1}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delays[attempt])
            
            except requests.exceptions.RequestException as e:
                print(f"  ⚠️ Request error: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delays[attempt])
            
            except Exception as e:
                print(f"  ❌ Unexpected error: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delays[attempt])
        
        # All retries failed
        print("  ❌ All retry attempts exhausted")
        return {
            "success": False,
            "error": "Failed to generate image after all retries"
        }
    
    def download_image(self, image_url: str) -> Path:
        """Download generated image"""
        print(f"⬇️  Downloading image...")
        
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        image_path = OUTPUT_DIR / f"{self.topic_slug}.png"
        
        try:
            response = requests.get(image_url, timeout=30)
            
            if response.status_code == 200:
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                
                file_size = image_path.stat().st_size
                print(f"  ✅ Downloaded image ({file_size:,} bytes)")
                return image_path
            else:
                print(f"  ❌ Download failed with status {response.status_code}")
                return None
                
        except Exception as e:
            print(f"  ❌ Download error: {e}")
            return None
    
    def save_metadata(self, image_path: Path, generation_result: Dict):
        """Save image metadata"""
        metadata = {
            "topic": self.topic,
            "prompt": self.prompt,
            "generated_at": datetime.now().isoformat(),
            "file_path": str(image_path.absolute()),
            "parameters": generation_result.get("parameters", {}),
            "success": generation_result.get("success", False)
        }
        
        metadata_path = OUTPUT_DIR / f"{self.topic_slug}_meta.json"
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved metadata to {metadata_path}")
    
    def validate_image(self, image_path: Path) -> bool:
        """Validate image file"""
        if not image_path or not image_path.exists():
            return False
        
        file_size = image_path.stat().st_size
        
        # Check minimum file size (100 KB)
        if file_size < 100 * 1024:
            print(f"  ⚠️ Image file too small ({file_size:,} bytes)")
            return False
        
        print(f"  ✅ Image validation passed")
        return True
    
    def run(self) -> Dict:
        """Main image generation workflow"""
        print(f"\n🖼️  Starting image generation for: {self.topic}\n")
        
        # Generate image
        result = self.generate_image()
        
        if not result.get("success"):
            print("\n❌ Image generation failed")
            return {
                "success": False,
                "error": result.get("error", "Unknown error")
            }
        
        # Download image
        image_url = result.get("image_url")
        image_path = self.download_image(image_url)
        
        # Validate
        if self.validate_image(image_path):
            # Save metadata
            self.save_metadata(image_path, result)
            
            return {
                "success": True,
                "image_path": str(image_path.absolute()),
                "topic": self.topic,
                "slug": self.topic_slug
            }
        else:
            return {
                "success": False,
                "error": "Image validation failed"
            }


def main():
    """Run image generation"""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python generate_topic_image.py <topic> <prompt>")
        print("Example: python generate_topic_image.py 'Quantum Computing' 'A colorful diagram...'")
        sys.exit(1)
    
    topic = sys.argv[1]
    prompt = ' '.join(sys.argv[2:])
    
    generator = ImageGenerator(topic, prompt)
    result = generator.run()
    
    # Display results
    print("\n" + "="*60)
    print(f"📊 IMAGE GENERATION RESULT: {topic}")
    print("="*60 + "\n")
    
    if result.get("success"):
        print(f"✅ Success!")
        print(f"📂 Image saved to: {result['image_path']}")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
