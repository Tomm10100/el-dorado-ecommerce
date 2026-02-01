"""
InnovLead Content Engine - Image Generation with Kei.ai Flux 2
Generates educational infographics using Kei.ai's Flux 2 model.

Per directive: directives/generate_topic_image.md
"""

import os
import sys
import json
import shutil

# Fix Unicode encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

import requests
from pathlib import Path
from typing import Dict
from datetime import datetime
import time

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration
OUTPUT_DIR = Path(".tmp/images")
KEI_AI_API_KEY = os.getenv("KEI_AI_API_KEY", "")
# Kei.ai correct base URL structure (per official docs)
KEI_AI_BASE_URL = "https://api.kie.ai/api/v1"
KEI_AI_TASK_URL = f"{KEI_AI_BASE_URL}/jobs/createTask"  # Create task endpoint
KEI_AI_QUERY_URL = f"{KEI_AI_BASE_URL}/jobs/recordInfo"  # Query task status (GET)


class KeiAiImageGenerator:
    def __init__(self, topic: str, prompt: str):
        self.topic = topic
        self.prompt = prompt
        self.topic_slug = self.create_slug(topic)
        self.max_retries = 3
        self.retry_delays = [5, 15, 30]
    
    def create_slug(self, text: str) -> str:
        """Create URL-friendly slug"""
        slug = text.lower()
        slug = ''.join(c if c.isalnum() or c == ' ' else '' for c in slug)
        slug = '-'.join(slug.split())
        return slug[:50]
    
    def generate_image(self) -> Dict:
        """Generate image using Google Imagen4 (Nano Banana) - Best text rendering"""
        print(f"🎨 Generating infographic for '{self.topic}' with Google Imagen4 (Nano Banana)...")
        
        if not KEI_AI_API_KEY:
            print("  ⚠️ No Kei.ai API key found")
            return {
                "success": False,
                "error": "KEI_AI_API_KEY not set. Get one at https://kie.ai"
            }
        
        try:
            # Step 1: Create task
            print(f"  Creating image generation task...")
            
            # Build input parameters - Using Google Imagen4 (Nano Banana)
            # Best-in-class text rendering - better than Flux or Ideogram
            input_params = {
                "prompt": self.prompt,
                "aspect_ratio": "1:1",  # Square for social media
                "num_images": "1",
                "negative_prompt": "blurry, low quality, distorted, ugly"
            }
            
            payload = {
                "model": "google/imagen4",  # Nano Banana - best for text
                "input": input_params
            }
            
            response = requests.post(
                KEI_AI_TASK_URL,
                json=payload,
                headers={
                    "Authorization": f"Bearer {KEI_AI_API_KEY}",
                    "Content-Type": "application/json"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                # Kei.ai returns {"code": 200, "data": {"taskId": "..."}}
                if data.get("code") == 200:
                    task_id = data.get("data", {}).get("taskId")
                    
                    if not task_id:
                        print(f"  ❌ No taskId returned")
                        return {"success": False, "error": "No taskId in response"}
                    
                    print(f"  ✅ Task created: {task_id}")
                else:
                    error_msg = data.get("msg", "Unknown error")
                    print(f"  ❌ API error: {error_msg}")
                    return {"success": False, "error": error_msg}
                
                # Step 2: Poll for results
                print(f"  Waiting for image generation...")
                image_url = self.wait_for_task(task_id)
                
                if image_url:
                    print(f"  ✅ Image generated successfully")
                    return {
                        "success": True,
                        "image_url": image_url,
                        "prompt_used": self.prompt,
                        "model": "google/imagen4",
                        "resolution": "1024x1024"
                    }
                else:
                    return {"success": False, "error": "Image generation timed out"}
            
            elif response.status_code == 401:
                print(f"  ❌ Invalid API key")
                return {"success": False, "error": "Invalid KEI_AI_API_KEY"}
            
            else:
                print(f"  ❌ API error: {response.status_code}")
                print(f"  Response: {response.text[:200]}")
                return {
                    "success": False,
                    "error": f"API returned {response.status_code}"
                }
                
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def wait_for_task(self, task_id: str, max_wait: int = 120) -> str:
        """Poll task status until complete"""
        start_time = time.time()
        
        while (time.time() - start_time) < max_wait:
            try:
                # Use GET request with query parameter (per official docs)
                response = requests.get(
                    f"{KEI_AI_QUERY_URL}?taskId={task_id}",
                    headers={
                        "Authorization": f"Bearer {KEI_AI_API_KEY}"
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    # Kei.ai returns {"code": 200, "data": {"state": "...", "resultJson": "{...}"}}
                    if data.get("code") == 200:
                        task_data = data.get("data", {})
                        state = task_data.get("state")
                        
                        if state == "success":
                            # Get image URL from resultJson
                            result_json_str = task_data.get("resultJson", "{}")
                            try:
                                result_json = json.loads(result_json_str)
                                result_urls = result_json.get("resultUrls", [])
                                if result_urls and len(result_urls) > 0:
                                    return result_urls[0]
                            except json.JSONDecodeError:
                                print(f"  ❌ Could not parse resultJson")
                                return None
                        
                        elif state == "fail":
                            fail_msg = task_data.get("failMsg", "Unknown error")
                            print(f"  ❌ Task failed: {fail_msg}")
                            return None
                        
                        # Still processing (waiting, queuing, generating), wait and retry
                        time.sleep(5)
                    else:
                        print(f"  ⚠️ Query returned code: {data.get('code')}")
                        time.sleep(5)
                else:
                    print(f"  ⚠️ Query failed: {response.status_code}")
                    time.sleep(5)
                    
            except Exception as e:
                print(f"  ⚠️ Polling error: {e}")
                time.sleep(5)
        
        print(f"  ⏱️ Timeout waiting for image generation")
        return None
    
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
            "service": "Kei.ai",
            "model": "Google Imagen4 (Nano Banana)",
            "resolution": generation_result.get("resolution", "1024x1024"),
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
        
        # Check minimum file size (50 KB)
        if file_size < 50 * 1024:
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
            print(f"\n❌ Image generation failed: {result.get('error')}")
            return result
        
        # Download image
        image_url = result.get("image_url")
        image_path = self.download_image(image_url)
        
        # Validate
        if self.validate_image(image_path):
            # Save metadata
            self.save_metadata(image_path, result)
            
            # Copy to InnovLead Documents folder for final outputs
            try:
                output_folder = Path.home() / "Desktop" / "InnovLead Documents" / "innovlead automatic content workflow final pictures"
                output_folder.mkdir(parents=True, exist_ok=True)
                final_path = output_folder / f"{self.topic_slug}.png"
                shutil.copy2(image_path, final_path)
                print(f"📋 Saved to InnovLead folder: {final_path.name}")
            except Exception as e:
                print(f"  ⚠️ Could not copy to InnovLead folder: {e}")
            
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
        print("Usage: python generate_image_keiai.py <topic> <prompt>")
        print("Example: python generate_image_keiai.py 'Quantum Computing' 'A colorful infographic...'")
        sys.exit(1)
    
    topic = sys.argv[1]
    prompt = ' '.join(sys.argv[2:])
    
    generator = KeiAiImageGenerator(topic, prompt)
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
