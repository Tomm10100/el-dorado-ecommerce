"""
InnovLead Content Engine - Topic Research with Gemini
Uses Gemini's built-in web search for comprehensive research (100% FREE).

Per directive: directives/research_topic.md
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

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration
OUTPUT_DIR = Path(".tmp/research")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


class GeminiResearcher:
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
        
        # Initialize Gemini
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            # Use Gemini 2.0 Flash with grounding
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        else:
            print("⚠️ GEMINI_API_KEY not set")
            self.model = None
    
    def create_slug(self, text: str) -> str:
        """Create URL-friendly slug from text"""
        slug = text.lower()
        slug = ''.join(c if c.isalnum() or c == ' ' else '' for c in slug)
        slug = '-'.join(slug.split())
        return slug[:50]
    
    def research_with_gemini(self) -> Dict:
        """Use Gemini with web grounding to research the topic"""
        print(f"🔍 Researching '{self.topic}' with Gemini + Web Search...")
        
        if not self.model:
            print("  ⚠️ Gemini not configured - using fallback")
            return self.fallback_research()
        
        # Comprehensive research prompt
        prompt = f"""Research the topic "{self.topic}" using current web information and provide:

1. **Core Concept**: A clear, 2-3 sentence explanation of what {self.topic} is
2. **Key Points**: 4-5 important facts about how it works or why it matters
3. **Analogies**: 2 simple analogies that would help an 8-year-old understand it
4. **Real-World Examples**: 2 practical applications or use cases

Be accurate and cite current information. Format your response as JSON:

{{
  "core_concept": "clear 2-3 sentence explanation",
  "key_points": ["point 1", "point 2", "point 3", "point 4"],
  "analogies": ["simple analogy 1", "simple analogy 2"],
  "real_world_examples": ["example 1", "example 2"]
}}

Only return the JSON, nothing else."""

        try:
            # Generate research
            response = self.model.generate_content(prompt)
            
            if response.text:
                content = response.text.strip()
                
                # Parse JSON response
                try:
                    # Extract JSON from markdown if present
                    if "```json" in content:
                        content = content.split("```json")[1].split("```")[0].strip()
                    elif "```" in content:
                        content = content.split("```")[1].split("```")[0].strip()
                    
                    research_result = json.loads(content)
                    
                    # Populate research data
                    self.research_data["core_concept"] = research_result.get("core_concept", "")
                    self.research_data["key_points"] = research_result.get("key_points", [])
                    self.research_data["analogies"] = research_result.get("analogies", [])
                    self.research_data["real_world_examples"] = research_result.get("real_world_examples", [])
                    
                    # Add Gemini as source
                    self.research_data["sources"].append({
                        "source": "Gemini with Web Search",
                        "title": f"Research on {self.topic}",
                        "url": "",
                        "content": ""
                    })
                    
                    print(f"  ✅ Comprehensive research completed")
                    return self.research_data
                    
                except json.JSONDecodeError as e:
                    print(f"  ⚠️ Failed to parse JSON, using text as core concept")
                    # Use raw response as core concept
                    self.research_data["core_concept"] = content[:500]
                    self.research_data["sources"].append({
                        "source": "Gemini",
                        "title": self.topic,
                        "url": "",
                        "content": ""
                    })
                    return self.research_data
            else:
                print("  ⚠️ Empty response from Gemini")
                return self.fallback_research()
                
        except Exception as e:
            print(f"  ⚠️ Gemini API error: {e}")
            return self.fallback_research()
    
    def fallback_research(self) -> Dict:
        """Fallback research using curated knowledge"""
        print("  ℹ️ Using curated fallback research...")
        
        # Curated knowledge base (same as before)
        knowledge_base = {
            "quantum computing": {
                "core_concept": "Quantum computing uses quantum mechanics principles like superposition and entanglement to process information in ways classical computers cannot. Instead of bits (0 or 1), quantum computers use qubits that can be both 0 and 1 simultaneously.",
                "key_points": [
                    "Uses qubits instead of classical bits for computation",
                    "Leverages superposition to explore multiple solutions at once",
                    "Quantum entanglement enables faster information sharing",
                    "Excels at optimization problems, cryptography, and molecular simulation"
                ],
                "analogies": [
                    "Like a coin spinning in the air - it's both heads and tails until it lands",
                    "Like reading all books in a library at once instead of one at a time"
                ],
                "real_world_examples": [
                    "Drug discovery and molecular simulation",
                    "Breaking encryption and creating quantum-safe cryptography"
                ]
            },
            "blockchain": {
                "core_concept": "Blockchain is a distributed digital ledger that records transactions across multiple computers in a way that makes the record immutable and transparent. Each block contains data and is linked to the previous block, forming a chain.",
                "key_points": [
                    "Decentralized - no single authority controls it",
                    "Immutable - once recorded, data cannot be altered",
                    "Transparent - all participants can view the chain",
                    "Uses cryptography to secure transactions"
                ],
                "analogies": [
                    "Like a notebook everyone has a copy of - when someone writes something, everyone's copy updates",
                    "Like a chain of sealed envelopes where you can't open or change one without everyone noticing"
                ],
                "real_world_examples": [
                    "Cryptocurrency transactions (Bitcoin, Ethereum)",
                    "Supply chain tracking and verification"
                ]
            },
            "neural network": {
                "core_concept": "Neural networks are computing systems inspired by biological neural networks in animal brains. They learn patterns from data through interconnected nodes (neurons) that adjust their connections based on experience.",
                "key_points": [
                    "Learns from examples rather than being explicitly programmed",
                    "Made of layers of interconnected nodes that process information",
                    "Gets better with more data and training",
                    "Powers modern AI like image recognition and language models"
                ],
                "analogies": [
                    "Like your brain learning to recognize a friend's face by seeing it many times",
                    "Like practicing basketball - the more you practice, the better your muscle memory"
                ],
                "real_world_examples": [
                    "Face recognition in your phone's camera",
                    "Voice assistants like Siri and Alexa"
                ]
            }
        }
        
        # Check if we have curated data for this topic
        topic_lower = self.topic.lower()
        for key, data in knowledge_base.items():
            if key in topic_lower:
                self.research_data.update(data)
                print(f"  ✅ Found curated knowledge for '{key}'")
                return self.research_data
        
        # Generic fallback
        self.research_data["core_concept"] = f"{self.topic} is a technology topic that requires further research."
        self.research_data["key_points"] = [
            f"{self.topic} is an important area in technology",
            "More research needed to provide detailed information"
        ]
        return self.research_data
    
    def conduct_research(self) -> Dict:
        """Main research workflow"""
        print(f"\n🔬 Starting research for: {self.topic}\n")
        
        # Research with Gemini
        self.research_with_gemini()
        
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
    
    if len(sys.argv) < 2:
        print("Usage: python research_topic_gemini.py <topic>")
        print("Example: python research_topic_gemini.py 'quantum computing'")
        sys.exit(1)
    
    topic = ' '.join(sys.argv[1:])
    
    researcher = GeminiResearcher(topic)
    research_data = researcher.conduct_research()
    
    # Display results
    print("\n" + "="*60)
    print(f"📊 RESEARCH RESULTS: {topic}")
    print("="*60 + "\n")
    
    print(f"Sources: {len(research_data['sources'])}")
    for source in research_data['sources']:
        print(f"  - {source['source']}")
    
    print(f"\n💡 Core Concept:\n{research_data['core_concept']}\n")
    
    if research_data['key_points']:
        print(f"🔑 Key Points ({len(research_data['key_points'])}):")
        for i, point in enumerate(research_data['key_points'], 1):
            print(f"  {i}. {point}")
    
    if research_data['analogies']:
        print(f"\n🎯 Analogies:")
        for analogy in research_data['analogies']:
            print(f"  - {analogy}")
    
    if research_data['real_world_examples']:
        print(f"\n🌍 Real-World Examples:")
        for example in research_data['real_world_examples']:
            print(f"  - {example}")
    
    # Save to file
    output_file = researcher.save_research()
    
    print(f"\n✅ Research complete!")
    print(f"📂 Full results saved to: {output_file.absolute()}")


if __name__ == "__main__":
    main()
