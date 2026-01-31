"""
InnovLead Content Engine - ELI5 Content Generation
Generates easy-to-understand explanations and image prompts from research data.

Per directive: directives/generate_eli5_content.md
"""

import os
import sys
import json

# Fix Unicode encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
from typing import Dict
import google.generativeai as genai


# Configuration
OUTPUT_DIR = Path(".tmp/content")

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
CONTENT_TYPE = os.getenv("CONTENT_TYPE", "social")  # 'social' or 'web'


class ContentGenerator:
    def __init__(self, research_file: str):
        self.research_file = Path(research_file)
        self.research_data = self.load_research()
        self.topic = self.research_data.get("topic", "Unknown Topic")
        self.topic_slug = self.create_slug(self.topic)
        
        # Initialize Gemini
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        else:
            print("⚠️ GEMINI_API_KEY not set - using fallback generation")
            self.model = None
    
    def create_slug(self, text: str) -> str:
        """Create URL-friendly slug"""
        slug = text.lower()
        slug = ''.join(c if c.isalnum() or c == ' ' else '' for c in slug)
        slug = '-'.join(slug.split())
        return slug[:50]
    
    def load_research(self) -> Dict:
        """Load research data from JSON"""
        with open(self.research_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_eli5_explanation(self) -> str:
        """Generate ELI5 (Explain Like I'm 5) explanation"""
        print(f"✍️ Generating ELI5 explanation for '{self.topic}'...")
        
        # Build context from research
        context = f"""
Topic: {self.topic}

Core Concept: {self.research_data.get('core_concept', '')}

Key Points:
{chr(10).join(f'- {point}' for point in self.research_data.get('key_points', []))}

Analogies:
{chr(10).join(f'- {analogy}' for analogy in self.research_data.get('analogies', []))}

Sources:
{chr(10).join(f'- {source.get("title", "")} ({source.get("source", "")})' for source in self.research_data.get('sources', []))}
"""
        
        # Adjust prompt based on content type
        if CONTENT_TYPE == "social":
            prompt = f"""You are an expert at creating engaging social media content explaining tech topics simply.

Based on this research about "{self.topic}":

{context}

Write a short, punchy social media caption/post that:
1. Is 100-150 words MAX (Instagram/TikTok length)
2. Uses simple language an 8-year-old could understand
3. Starts with a hook/question to grab attention
4. Includes 1-2 relatable analogies
5. Ends with a thought-provoking statement or call-to-action
6. Is engaging, shareable, and educational

Write ONLY the post text, no hashtags or emojis yet:"""
        else:
            prompt = f"""You are an expert at explaining complex technical topics in simple terms that an 8-year-old could understand.

Based on this research about "{self.topic}":

{context}

Write a clear, engaging ELI5 (Explain Like I'm 5) explanation that:
1. Uses simple language and everyday analogies
2. Is between 150-250 words
3. Avoids jargon or explains it simply
4. Makes the topic interesting and relatable
5. Is accurate but accessible

Write ONLY the explanation, no title or extra formatting:"""

        if self.model:
            try:
                response = self.model.generate_content(prompt)
                explanation = response.text.strip()
                print(f"  ✅ Generated {len(explanation)} character explanation")
                return explanation
            except Exception as e:
                print(f"  ⚠️ Error calling Gemini API: {e}")
                return self.fallback_explanation()
        else:
            return self.fallback_explanation()
    
    def fallback_explanation(self) -> str:
        """Fallback explanation when API unavailable"""
        core = self.research_data.get('core_concept', 'No information available')
        analogies = self.research_data.get('analogies', [])
        
        explanation = f"{core}\n\n"
        
        if analogies:
            explanation += f"Think of it like this: {analogies[0]}\n\n"
        
        key_points = self.research_data.get('key_points', [])[:3]
        if key_points:
            explanation += "Here's why it matters:\n"
            for point in key_points:
                explanation += f"- {point}\n"
        
        return explanation
    
    def generate_image_prompt(self) -> str:
        """Generate detailed image prompt for visualization"""
        print(f"🎨 Generating image prompt...")
        
        prompt_template = f"""You are an expert at creating detailed image generation prompts for educational illustrations.

Create a detailed image generation prompt for an illustration explaining "{self.topic}" that:
1. Would help an 8-year-old understand the concept visually
2. Uses clear, simple visual metaphors or diagrams
3. Is colorful, engaging, and educational
4. Could be an infographic, diagram, or illustrated analogy
5. Is detailed enough for an AI image generator (100+ words)

Topic context:
{self.research_data.get('core_concept', '')}

Analogies to consider:
{', '.join(self.research_data.get('analogies', []))}

Write ONLY the image generation prompt, make it detailed and specific:"""

        if self.model:
            try:
                response = self.model.generate_content(prompt_template)
                image_prompt = response.text.strip()
                print(f"  ✅ Generated {len(image_prompt)} character image prompt")
                return image_prompt
            except Exception as e:
                print(f"  ⚠️ Error calling Gemini API: {e}")
                return self.fallback_image_prompt()
        else:
            return self.fallback_image_prompt()
    
    def fallback_image_prompt(self) -> str:
        """Fallback image prompt"""
        analogies = self.research_data.get('analogies', [])
        
        if analogies:
            base_prompt = f"An educational illustration showing {self.topic} explained with the analogy: {analogies[0]}. Colorful, simple, diagram-style, easy to understand for children, infographic style, clear labels, professional educational design."
        else:
            base_prompt = f"An educational infographic explaining {self.topic} in simple visual terms. Colorful diagram, clear labels, simple illustrations, professional design, suitable for children, engaging and informative."
        
        return base_prompt
    
    def extract_tags(self) -> list[str]:
        """Extract relevant tags from topic"""
        print("🏷️ Extracting tags...")
        
        # Basic tag extraction
        tags = []
        
        # Add topic words as tags
        words = self.topic.lower().split()
        tags.extend([w for w in words if len(w) > 3])
        
        # Add category tags
        categories = {
            "ai": ["ai", "artificial-intelligence", "machine-learning"],
            "blockchain": ["blockchain", "cryptocurrency", "web3"],
            "quantum": ["quantum", "quantum-computing", "physics"],
            "programming": ["programming", "coding", "software"],
            "security": ["security", "cybersecurity", "encryption"],
            "cloud": ["cloud", "cloud-computing", "infrastructure"]
        }
        
        for key, category_tags in categories.items():
            if key in self.topic.lower():
                tags.extend(category_tags[:2])
        
        # Add general tags
        tags.extend(["tech", "explained", "eli5", "technology"])
        
        # Deduplicate and limit
        unique_tags = list(dict.fromkeys(tags))[:10]
        
        print(f"  ✅ Extracted {len(unique_tags)} tags")
        return unique_tags
    
    def generate_content(self) -> Dict:
        """Main content generation workflow"""
        print(f"\n📝 Generating content for: {self.topic}\n")
        
        explanation = self.generate_eli5_explanation()
        image_prompt = self.generate_image_prompt()
        tags = self.extract_tags()
        
        content_data = {
            "topic": self.topic,
            "slug": self.topic_slug,
            "explanation": explanation,
            "image_prompt": image_prompt,
            "tags": tags,
            "sources": [s.get("url", "") for s in self.research_data.get("sources", [])],
            "created_at": None  # Will be set when saving
        }
        
        return content_data
    
    def save_content(self, content_data: Dict):
        """Save content to JSON file"""
        from datetime import datetime
        
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        content_data["created_at"] = datetime.now().isoformat()
        
        output_file = OUTPUT_DIR / f"{self.topic_slug}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(content_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Saved content to {output_file}")
        return output_file


def main():
    """Run content generation"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python generate_eli5_content.py <research_file>")
        print("Example: python generate_eli5_content.py .tmp/research/quantum-computing.json")
        sys.exit(1)
    
    research_file = sys.argv[1]
    
    if not Path(research_file).exists():
        print(f"❌ Research file not found: {research_file}")
        sys.exit(1)
    
    generator = ContentGenerator(research_file)
    content_data = generator.generate_content()
    
    # Display results
    print("\n" + "="*60)
    print(f"📊 GENERATED CONTENT: {content_data['topic']}")
    print("="*60 + "\n")
    
    print(f"Slug: {content_data['slug']}\n")
    
    print(f"Explanation ({len(content_data['explanation'])} chars):")
    print(content_data['explanation'][:200] + "..." if len(content_data['explanation']) > 200 else content_data['explanation'])
    print()
    
    print(f"Image Prompt ({len(content_data['image_prompt'])} chars):")
    print(content_data['image_prompt'][:150] + "...")
    print()
    
    print(f"Tags: {', '.join(content_data['tags'])}\n")
    
    # Save to file
    output_file = generator.save_content(content_data)
    
    print(f"✅ Content generation complete!")
    print(f"📂 Full results saved to: {output_file.absolute()}")


if __name__ == "__main__":
    main()
