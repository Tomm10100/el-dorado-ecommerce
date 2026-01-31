"""
InnovLead Content Engine - Checkpoint Test
Runs content creation workflow and saves results to Desktop for review.
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

# Fix Unicode encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

import subprocess


class CheckpointTest:
    def __init__(self, topic: str):
        self.topic = topic
        self.desktop = Path.home() / "Desktop"
        self.output_folder = self.desktop / f"InnovLead_Test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.tmp_dir = Path(".tmp")
        
    def create_output_folder(self):
        """Create timestamped folder on Desktop"""
        self.output_folder.mkdir(exist_ok=True)
        print(f"📁 Created output folder: {self.output_folder}")
        return self.output_folder
    
    def run_script(self, script_name: str, args: list = None):
        """Run a Python script and capture output"""
        cmd = [sys.executable, f"execution/{script_name}"]
        if args:
            cmd.extend(args)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=120
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def run_test(self):
        """Run complete checkpoint test"""
        print("\n" + "="*70)
        print("🧪 CHECKPOINT TEST - Content Creation Workflow")
        print("="*70 + "\n")
        
        print(f"📝 Topic: {self.topic}")
        print(f"📂 Output: {self.output_folder}\n")
        
        # Create output folder
        self.create_output_folder()
        
        # Step 1: Research
        print("─" * 70)
        print("STEP 1/3: Research Topic with Gemini")
        print("─" * 70)
        
        result = self.run_script("research_topic_gemini.py", [self.topic])
        
        if result["success"]:
            print("✅ Research completed")
            
            # Find and copy research file
            slug = self.topic.lower().replace(' ', '-')[:50]
            research_file = self.tmp_dir / "research" / f"{slug}.json"
            
            if research_file.exists():
                dest = self.output_folder / f"1_research_{slug}.json"
                shutil.copy(research_file, dest)
                print(f"📄 Saved: {dest.name}")
        else:
            print(f"❌ Research failed: {result.get('error', 'Unknown error')}")
            return False
        
        # Step 2: Generate Content
        print("\n" + "─" * 70)
        print("STEP 2/3: Generate Social Media Content")
        print("─" * 70)
        
        result = self.run_script("generate_eli5_content.py", [str(research_file)])
        
        if result["success"]:
            print("✅ Content generated")
            
            # Find and copy content file
            content_file = self.tmp_dir / "content" / f"{slug}.json"
            
            if content_file.exists():
                # Copy JSON
                dest_json = self.output_folder / f"2_content_{slug}.json"
                shutil.copy(content_file, dest_json)
                
                # Also create readable text file
                with open(content_file, 'r', encoding='utf-8') as f:
                    content_data = json.load(f)
                
                dest_txt = self.output_folder / f"2_content_{slug}.txt"
                with open(dest_txt, 'w', encoding='utf-8') as f:
                    f.write(f"TOPIC: {content_data.get('topic', 'Unknown')}\n\n")
                    f.write("="*70 + "\n")
                    f.write("SOCIAL MEDIA POST\n")
                    f.write("="*70 + "\n\n")
                    f.write(content_data.get('explanation', 'No content'))
                    f.write("\n\n" + "="*70 + "\n")
                    f.write("HASHTAGS\n")
                    f.write("="*70 + "\n\n")
                    tags = content_data.get('tags', [])
                    f.write(' '.join([f'#{tag}' for tag in tags]))
                    f.write("\n\n" + "="*70 + "\n")
                    f.write("IMAGE PROMPT\n")
                    f.write("="*70 + "\n\n")
                    f.write(content_data.get('image_prompt', 'No prompt'))
                
                print(f"📄 Saved: {dest_json.name}")
                print(f"📄 Saved: {dest_txt.name}")
        else:
            print(f"❌ Content generation failed: {result.get('error', 'Unknown error')}")
            return False
        
        # Step 3: Generate Image
        print("\n" + "─" * 70)
        print("STEP 3/3: Generate Image with Kei.ai Flux 2")
        print("─" * 70)
        
        # Load content to get image prompt
        with open(content_file, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
            image_prompt = content_data.get('image_prompt', 'Educational infographic')
        
        result = self.run_script("generate_image_keiai.py", [self.topic, image_prompt])
        
        if result["success"]:
            print("✅ Image generated")
            
            # Find and copy image
            image_file = self.tmp_dir / "images" / f"{slug}.png"
            
            if image_file.exists():
                dest = self.output_folder / f"3_image_{slug}.png"
                shutil.copy(image_file, dest)
                print(f"🖼️  Saved: {dest.name}")
        else:
            print(f"⚠️  Image generation failed (but content is ready): {result.get('error', 'Unknown error')}")
            # Continue - content is still usable
        
        # Create summary
        self.create_summary()
        
        return True
    
    def create_summary(self):
        """Create summary file with all details"""
        summary_file = self.output_folder / "README.txt"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("INNOVLEAD CONTENT ENGINE - CHECKPOINT TEST RESULTS\n")
            f.write("="*70 + "\n\n")
            f.write(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Topic: {self.topic}\n\n")
            f.write("="*70 + "\n")
            f.write("FILES IN THIS FOLDER\n")
            f.write("="*70 + "\n\n")
            f.write("1_research_*.json    - Research data from Gemini\n")
            f.write("2_content_*.json     - Generated social media post (JSON)\n")
            f.write("2_content_*.txt      - Generated social media post (Readable)\n")
            f.write("3_image_*.png        - Generated infographic (if successful)\n")
            f.write("README.txt           - This file\n\n")
            f.write("="*70 + "\n")
            f.write("NEXT STEPS\n")
            f.write("="*70 + "\n\n")
            f.write("1. Open '2_content_*.txt' to see your social media post\n")
            f.write("2. View '3_image_*.png' to see the infographic\n")
            f.write("3. Copy the text and post manually to Instagram/TikTok/Facebook\n")
            f.write("4. Attach the image when posting\n\n")
            f.write("="*70 + "\n")
            f.write("WORKFLOW STATUS\n")
            f.write("="*70 + "\n\n")
            
            # Check what was created
            files = list(self.output_folder.glob("*"))
            research_ok = any("1_research" in f.name for f in files)
            content_ok = any("2_content" in f.name for f in files)
            image_ok = any("3_image" in f.name for f in files)
            
            f.write(f"✅ Research:        {'SUCCESS' if research_ok else 'FAILED'}\n")
            f.write(f"✅ Content:         {'SUCCESS' if content_ok else 'FAILED'}\n")
            f.write(f"{'✅' if image_ok else '⚠️ '} Image:           {'SUCCESS' if image_ok else 'FAILED (needs KEI_AI_API_KEY in .env)'}\n\n")
            
            if research_ok and content_ok:
                f.write("🎉 CHECKPOINT TEST PASSED!\n")
                f.write("Your content creation workflow is working correctly.\n\n")
            else:
                f.write("⚠️  CHECKPOINT TEST INCOMPLETE\n")
                f.write("Please check error messages in console.\n\n")
        
        print(f"\n📄 Summary saved: {summary_file.name}")


def main():
    """Run checkpoint test"""
    
    if len(sys.argv) < 2:
        topic = "Neural Networks"  # Default test topic
        print(f"ℹ️  No topic provided, using default: '{topic}'")
    else:
        topic = ' '.join(sys.argv[1:])
    
    tester = CheckpointTest(topic)
    success = tester.run_test()
    
    # Final summary
    print("\n" + "="*70)
    print("🏁 CHECKPOINT TEST COMPLETE")
    print("="*70 + "\n")
    
    if success:
        print(f"✅ Results saved to Desktop:")
        print(f"📂 {tester.output_folder}\n")
        print("Open that folder to see:")
        print("  • Research data (JSON)")
        print("  • Social media post (TXT)")
        print("  • Infographic image (PNG)")
        print("  • Summary (README.txt)")
        print("\n💡 Next: Review the content and test posting manually to social media")
    else:
        print("❌ Checkpoint test failed. Check error messages above.")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
