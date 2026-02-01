"""
InnovLead Content Engine - Topic Research
Researches a tech topic in depth gathering information from multiple sources.

Per directive: directives/research_topic.md
"""

import os
import sys
import json

# Fix Unicode encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

import requests
from pathlib import Path
from typing import Dict, List
import urllib.parse


# Configuration
OUTPUT_DIR = Path(".tmp/research")
MAX_SOURCES = 5  # Maximum sources to gather


class TopicResearcher:
    def __init__(self, topic: str):
        self.topic = topic
        self.topic_slug = self.create_slug(topic)
        self.research_data = {
            "topic": topic,
            "sources": [],
            "core_concept": "",
            "key_points": [],
            "analogies": [],
            "real_world_examples": []
        }
    
    def create_slug(self, text: str) -> str:
        """Create URL-friendly slug from text"""
        slug = text.lower()
        slug = ''.join(c if c.isalnum() or c == ' ' else '' for c in slug)
        slug = '-'.join(slug.split())
        return slug[:50]  # Limit length
    
    def search_wikipedia(self) -> Dict:
        """Search Wikipedia for topic information"""
        print(f"📖 Searching Wikipedia for '{self.topic}'...")
        
        try:
            # Search for the topic
            search_url = "https://en.wikipedia.org/w/api.php"
            search_params = {
                "action": "query",
                "list": "search",
                "srsearch": self.topic,
                "format": "json",
                "utf8": 1
            }
            
            response = requests.get(search_url, params=search_params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                search_results = data.get("query", {}).get("search", [])
                
                if search_results:
                    # Get the top result
                    page_title = search_results[0]["title"]
                    
                    # Fetch page content
                    content_params = {
                        "action": "query",
                        "titles": page_title,
                        "prop": "extracts",
                        "exintro": True,
                        "explaintext": True,
                        "format": "json",
                        "utf8": 1
                    }
                    
                    content_response = requests.get(search_url, params=content_params, timeout=10)
                    
                    if content_response.status_code == 200:
                        content_data = content_response.json()
                        pages = content_data.get("query", {}).get("pages", {})
                        
                        if pages:
                            page = list(pages.values())[0]
                            extract = page.get("extract", "")[:1000]  # First 1000 chars
                            
                            print(f"  ✅ Found Wikipedia article: {page_title}")
                            
                            return {
                                "source": "Wikipedia",
                                "title": page_title,
                                "url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(page_title)}",
                                "content": extract
                            }
                            
        except Exception as e:
            print(f"  ⚠️ Error searching Wikipedia: {e}")
        
        return None
    
    def search_web_summary(self) -> List[Dict]:
        """Generate web search summary (placeholder - would use real search API)"""
        print(f"🌐 Searching web for '{self.topic}'...")
        
        # TODO: Integrate with actual search API (Google Custom Search, Brave Search, etc.)
        # For now, return placeholder
        
        print("  ℹ️ Web search not yet implemented (requires API key)")
        return []
    
    def extract_key_information(self):
        """Extract and structure key information from gathered sources"""
        print("🔍 Extracting key information...")
        
        all_content = ""
        for source in self.research_data["sources"]:
            all_content += source.get("content", "") + "\n\n"
        
        if not all_content:
            print("  ⚠️ No content to analyze")
            return
        
        # Simple extraction (in real implementation, use LLM to analyze)
        # For now, use first source as core concept
        if self.research_data["sources"]:
            first_source = self.research_data["sources"][0]
            content = first_source.get("content", "")
            
            # Take first 2-3 sentences as core concept
            sentences = content.split('. ')
            self.research_data["core_concept"] = '. '.join(sentences[:2]) + '.'
            
            # Extract key points (simple: every sentence with certain keywords)
            keywords = ["is", "are", "uses", "works", "allows", "enables", "provides"]
            key_points = []
            
            for sentence in sentences[2:]:
                if any(kw in sentence.lower() for kw in keywords):
                    key_points.append(sentence.strip())
                    if len(key_points) >= 5:
                        break
            
            self.research_data["key_points"] = key_points
            
        print(f"  ✅ Extracted core concept and {len(self.research_data['key_points'])} key points")
    
    def add_curated_analogies(self):
        """Add curated analogies for common topics"""
        print("💡 Adding analogies...")
        
        # Curated analogies for common tech topics
        analogy_map = {
            "blockchain": "Like a notebook that everyone has a copy of, and everyone can see when someone writes something new",
            "neural network": "Like your brain learning to recognize your friend's face by seeing it many times",
            "quantum computing": "Like a coin spinning in the air - it's both heads and tails until it lands",
            "docker": "Like a lunch box that has everything you need for lunch, so you can eat anywhere",
            "encryption": "Like a secret language only you and your friend understand",
            "api": "Like a waiter at a restaurant - you tell them what you want, they bring it from the kitchen",
            "cloud computing": "Like storing your toys at a friend's house instead of your room",
        }
        
        # Find matching analogy
        for key, analogy in analogy_map.items():
            if key in self.topic.lower():
                self.research_data["analogies"].append(analogy)
                print(f"  ✅ Added analogy for '{key}'")
                break
        
        if not self.research_data["analogies"]:
            print("  ℹ️ No curated analogy found for this topic")
    
    def conduct_research(self) -> Dict:
        """Main research workflow"""
        print(f"\n🔬 Starting research for: {self.topic}\n")
        
        # Gather from sources
        wiki_data = self.search_wikipedia()
        if wiki_data:
            self.research_data["sources"].append(wiki_data)
        
        web_data = self.search_web_summary()
        self.research_data["sources"].extend(web_data)
        
        # Extract and structure information
        if self.research_data["sources"]:
            self.extract_key_information()
            self.add_curated_analogies()
        else:
            print("  ⚠️ No sources found - research incomplete")
        
        return self.research_data
    
    def save_research(self):
        """Save research to JSON file"""
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        output_file = OUTPUT_DIR / f"{self.topic_slug}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.research_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Saved research to {output_file}")
        return output_file


def main():
    """Run topic research"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python research_topic_deep.py <topic>")
        print("Example: python research_topic_deep.py 'quantum computing'")
        sys.exit(1)
    
    topic = ' '.join(sys.argv[1:])
    
    researcher = TopicResearcher(topic)
    research_data = researcher.conduct_research()
    
    # Display results
    print("\n" + "="*60)
    print(f"📊 RESEARCH RESULTS: {topic}")
    print("="*60 + "\n")
    
    print(f"Sources found: {len(research_data['sources'])}")
    for source in research_data['sources']:
        print(f"  - {source['source']}: {source['title']}")
    
    print(f"\nCore Concept:\n{research_data['core_concept']}\n")
    
    if research_data['key_points']:
        print(f"Key Points ({len(research_data['key_points'])}):")
        for i, point in enumerate(research_data['key_points'], 1):
            print(f"  {i}. {point}")
    
    if research_data['analogies']:
        print(f"\nAnalogies:")
        for analogy in research_data['analogies']:
            print(f"  - {analogy}")
    
    # Save to file
    output_file = researcher.save_research()
    
    print(f"\n✅ Research complete!")
    print(f"📂 Full results saved to: {output_file.absolute()}")


if __name__ == "__main__":
    main()
