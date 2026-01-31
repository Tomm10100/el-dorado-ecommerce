"""
InnovLead Content Engine - Performance Monitor
Tracks content generation stats and API usage.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Fix Unicode encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')


class ContentMonitor:
    def __init__(self):
        self.tmp_dir = Path(".tmp")
        self.research_dir = self.tmp_dir / "research"
        self.content_dir = self.tmp_dir / "content"
        self.images_dir = self.tmp_dir / "images"
        self.published_dir = self.tmp_dir / "published"
    
    def count_files(self, directory):
        """Count JSON files in directory"""
        if not directory.exists():
            return 0
        return len(list(directory.glob("*.json")))
    
    def count_images(self):
        """Count generated images"""
        if not self.images_dir.exists():
            return 0
        return len(list(self.images_dir.glob("*.png")))
    
    def get_recent_topics(self, limit=10):
        """Get most recent topics"""
        if not self.content_dir.exists():
            return []
        
        files = sorted(
            self.content_dir.glob("*.json"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        topics = []
        for file in files[:limit]:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    topics.append({
                        'topic': data.get('topic', 'Unknown'),
                        'date': datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M'),
                        'has_image': (self.images_dir / f"{file.stem}.png").exists()
                    })
            except Exception:
                continue
        
        return topics
    
    def get_api_usage_estimate(self):
        """Estimate API usage based on content count"""
        total_content = self.count_files(self.content_dir)
        total_images = self.count_images()
        
        # Gemini: Free tier (no cost tracking needed)
        # Ideogram: 100 free/month
        ideogram_remaining = max(0, 100 - total_images)
        
        return {
            'gemini_calls': total_content * 2,  # Research + Content
            'ideogram_used': total_images,
            'ideogram_remaining': ideogram_remaining,
            'ideogram_percentage': (total_images / 100) * 100
        }
    
    def generate_report(self):
        """Generate performance report"""
        print("\n" + "="*60)
        print("📊 INNOVLEAD CONTENT ENGINE - PERFORMANCE REPORT")
        print("="*60 + "\n")
        
        # File counts
        research_count = self.count_files(self.research_dir)
        content_count = self.count_files(self.content_dir)
        image_count = self.count_images()
        published_count = self.count_files(self.published_dir)
        
        print("📁 Content Statistics:")
        print(f"  Research files:  {research_count}")
        print(f"  Content posts:   {content_count}")
        print(f"  Images created:  {image_count}")
        print(f"  Published:       {published_count}")
        
        # API Usage
        print("\n💰 API Usage:")
        usage = self.get_api_usage_estimate()
        print(f"  Gemini calls:    {usage['gemini_calls']} (FREE ✅)")
        print(f"  Ideogram used:   {usage['ideogram_used']}/100 ({usage['ideogram_percentage']:.1f}%)")
        print(f"  Remaining free:  {usage['ideogram_remaining']} images")
        
        # Cost
        cost = 0
        if usage['ideogram_used'] > 100:
            cost = 8  # Basic plan
        
        print(f"\n💵 Monthly Cost:   ${cost}")
        print(f"   Annual Cost:    ${cost * 12}")
        print(f"   Savings vs Old: ${300 - (cost * 12)}/year")
        
        # Recent topics
        print("\n📝 Recent Topics:")
        recent = self.get_recent_topics(5)
        if recent:
            for topic in recent:
                status = "🎨" if topic['has_image'] else "📝"
                print(f"  {status} {topic['topic']}")
                print(f"     {topic['date']}")
        else:
            print("  No content generated yet. Run the pipeline!")
        
        # Health check
        print("\n🏥 System Health:")
        checks = {
            "Research working": research_count > 0,
            "Content generation working": content_count > 0,
            "Image generation working": image_count > 0,
            "Publishing configured": published_count > 0 or (self.tmp_dir / "social_publications.jsonl").exists()
        }
        
        for check, status in checks.items():
            symbol = "✅" if status else "⚠️"
            print(f"  {symbol} {check}")
        
        # Recommendations
        print("\n💡 Recommendations:")
        
        if usage['ideogram_percentage'] > 80:
            print("  ⚠️ Close to Ideogram free tier limit (80%+)")
            print("     Consider upgrading to Basic ($8/mo) for 400 images")
        
        if content_count == 0:
            print("  ℹ️ No content generated yet")
            print("     Run: python execution\\main_content_pipeline.py \"Topic\"")
        
        if content_count > 0 and published_count == 0:
            print("  ℹ️ Content created but not published")
            print("     Check social_queue.json or configure publishing endpoint")
        
        if content_count >= 5 and image_count == 0:
            print("  ⚠️ Missing images for content")
            print("     Add IDEOGRAM_API_KEY to .env")
        
        print("\n" + "="*60)
        print(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60 + "\n")


def main():
    """Run performance monitor"""
    monitor = ContentMonitor()
    monitor.generate_report()


if __name__ == "__main__":
    main()
