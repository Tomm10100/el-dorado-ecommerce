"""
InnovLead Content Engine - Main Pipeline Orchestrator
Runs the complete content creation and publishing workflow.

Per directive: directives/run_content_pipeline.md
"""

import sys
import json
import os

# Fix Unicode encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import uuid


# Configuration
PIPELINE_LOG = Path(".tmp/pipeline_log.jsonl")


class ContentPipeline:
    def __init__(self, specific_topic: Optional[str] = None):
        self.run_id = str(uuid.uuid4())[:8]
        self.specific_topic = specific_topic
        self.start_time = datetime.now()
        self.steps_completed = []
        self.current_topic = None
        self.current_slug = None
    
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "ℹ️ ",
            "SUCCESS": "✅",
            "ERROR": "❌",
            "WARNING": "⚠️ "
        }.get(level, "")
        
        print(f"[{timestamp}] {prefix} {message}")
    
    def run_script(self, script_name: str, args: list = None) -> Dict:
        """Run a Python script and return result"""
        args = args or []
        cmd = [sys.executable, f"execution/{script_name}"] + args
        
        self.log(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Script timeout (>2 minutes)"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def step_discover_topics(self) -> bool:
        """Step 1: Discover trending topics"""
        self.log("Step 1/6: Discovering trending topics...", "INFO")
        
        result = self.run_script("discover_trending_topics.py")
        
        if result["success"]:
            self.steps_completed.append("discover")
            self.log("Topic discovery complete", "SUCCESS")
            return True
        else:
            self.log(f"Topic discovery failed: {result.get('error', 'Unknown')}", "ERROR")
            return False
    
    def step_select_topic(self) -> bool:
        """Step 2: Select best topic from discovered list"""
        self.log("Step 2/6: Selecting topic...", "INFO")
        
        if self.specific_topic:
            self.current_topic = self.specific_topic
            self.log(f"Using specified topic: {self.current_topic}", "INFO")
            return True
        
        # Load discovered topics
        topics_file = Path(".tmp/trending_topics.json")
        
        if not topics_file.exists():
            self.log("No topics file found", "ERROR")
            return False
        
        with open(topics_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            topics = data.get("topics", [])
        
        if not topics:
            self.log("No topics available", "ERROR")
            return False
        
        # Select highest scored topic
        self.current_topic = topics[0]["title"]
        self.log(f"Selected topic: {self.current_topic} (score: {topics[0]['score']})", "SUCCESS")
        
        return True
    
    def step_research_topic(self) -> bool:
        """Step 3: Research the selected topic"""
        self.log("Step 3/6: Researching topic with Gemini...", "INFO")
        
        # Use Gemini by default (FREE), Perplexity if key is set
        perplexity_key = os.getenv("PERPLEXITY_API_KEY", "")
        
        if perplexity_key:
            self.log("  Using Perplexity (premium research)", "INFO")
            result = self.run_script("research_topic_perplexity.py", [self.current_topic])
        else:
            self.log("  Using Gemini with web search (free)", "INFO")
            result = self.run_script("research_topic_gemini.py", [self.current_topic])
        
        if result["success"]:
            # Get the slug from the research output
            slug = self.create_slug(self.current_topic)
            research_file = Path(f".tmp/research/{slug}.json")
            
            if research_file.exists():
                self.current_slug = slug
                self.steps_completed.append("research")
                self.log("Research complete", "SUCCESS")
                return True
        
        self.log(f"Research failed: {result.get('error', 'Unknown')}", "ERROR")
        return False
    
    def step_generate_content(self) -> bool:
        """Step 4: Generate ELI5 content and image prompt"""
        self.log("Step 4/6: Generating ELI5 content...", "INFO")
        
        research_file = f".tmp/research/{self.current_slug}.json"
        
        result = self.run_script("generate_eli5_content.py", [research_file])
        
        if result["success"]:
            content_file = Path(f".tmp/content/{self.current_slug}.json")
            
            if content_file.exists():
                self.steps_completed.append("generate")
                self.log("Content generation complete", "SUCCESS")
                return True
        
        self.log(f"Content generation failed: {result.get('error', 'Unknown')}", "ERROR")
        return False
    
    def step_generate_image(self) -> bool:
        """Step 5: Generate visual image with Kei.ai Flux 2"""
        self.log("Step 5/6: Generating image with Kei.ai Flux 2...", "INFO")
        
        # Load content to get image prompt
        content_file = Path(f".tmp/content/{self.current_slug}.json")
        
        with open(content_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
            image_prompt = content.get("image_prompt", "")
        
        result = self.run_script("generate_image_keiai.py", [self.current_topic, image_prompt])
        
        if result["success"]:
            self.steps_completed.append("image")
            self.log("Image generation complete", "SUCCESS")
            return True
        else:
            self.log("Image generation failed, continuing without image...", "WARNING")
            # Don't fail the pipeline, just continue without image
            return True
    
    def step_publish_content(self) -> bool:
        """Step 6: Publish to social media"""
        self.log("Step 6/6: Publishing to social media...", "INFO")
        
        content_file = f".tmp/content/{self.current_slug}.json"
        image_file = f".tmp/images/{self.current_slug}.png"
        
        args = [content_file]
        if Path(image_file).exists():
            args.append(image_file)
        
        result = self.run_script("publish_to_social.py", args)
        
        if result["success"]:
            self.steps_completed.append("publish")
            self.log("Publishing complete", "SUCCESS")
            return True
        
        self.log(f"Publishing failed: {result.get('error', 'Unknown')}", "ERROR")
        return False
    
    def create_slug(self, text: str) -> str:
        """Create URL-friendly slug"""
        slug = text.lower()
        slug = ''.join(c if c.isalnum() or c == ' ' else '' for c in slug)
        slug = '-'.join(slug.split())
        return slug[:50]
    
    def save_pipeline_log(self, status: str, published_url: str = ""):
        """Save pipeline execution log"""
        duration = (datetime.now() - self.start_time).total_seconds()
        
        log_entry = {
            "run_id": self.run_id,
            "timestamp": self.start_time.isoformat(),
            "topic": self.current_topic,
            "slug": self.current_slug,
            "status": status,
            "published_url": published_url,
            "steps_completed": self.steps_completed,
            "duration_seconds": round(duration, 2)
        }
        
        PIPELINE_LOG.parent.mkdir(parents=True, exist_ok=True)
        
        with open(PIPELINE_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def run(self) -> bool:
        """Execute complete pipeline"""
        self.log(f"🚀 Starting Content Pipeline (Run ID: {self.run_id})", "INFO")
        print("="*60)
        
        try:
            # Step 1: Discover topics (skip if specific topic provided)
            if not self.specific_topic:
                if not self.step_discover_topics():
                    self.save_pipeline_log("failed - discovery")
                    return False
            
            # Step 2: Select topic
            if not self.step_select_topic():
                self.save_pipeline_log("failed - selection")
                return False
            
            # Step 3: Research
            if not self.step_research_topic():
                self.save_pipeline_log("failed - research")
                return False
            
            # Step 4: Generate content
            if not self.step_generate_content():
                self.save_pipeline_log("failed - content generation")
                return False
            
            # Step 5: Generate image
            if not self.step_generate_image():
                # Continue even if image fails
                pass
            
            # Step 6: Publish
            if not self.step_publish_content():
                self.save_pipeline_log("failed - publishing")
                return False
            
            # Success!
            published_url = f"https://media-uploader--tommy0110.replit.app/topics/{self.current_slug}.html"
            self.save_pipeline_log("success", published_url)
            
            duration = (datetime.now() - self.start_time).total_seconds()
            
            print("="*60)
            self.log(f"✅ PIPELINE COMPLETE! ({duration:.1f}s)", "SUCCESS")
            self.log(f"📄 Topic: {self.current_topic}", "INFO")
            self.log(f"🌐 Published URL: {published_url}", "INFO")
            print("="*60)
            
            return True
            
        except Exception as e:
            self.log(f"Pipeline crashed: {e}", "ERROR")
            self.save_pipeline_log(f"crashed - {str(e)}")
            return False


def main():
    """Run content pipeline"""
    specific_topic = None
    
    if len(sys.argv) > 1:
        specific_topic = ' '.join(sys.argv[1:])
        print(f"📌 Running pipeline for specific topic: {specific_topic}\n")
    else:
        print("🔄 Running automated pipeline (will discover trending topics)\n")
    
    pipeline = ContentPipeline(specific_topic=specific_topic)
    success = pipeline.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
