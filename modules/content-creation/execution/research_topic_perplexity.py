"""
InnovLead Content Engine - Topic Research (Perplexity)
Researches a tech topic using Perplexity AI for comprehensive information.

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
from typing import Dict

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration
OUTPUT_DIR = Path(".tmp/research")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"


class PerplexityResearcher:
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
        return slug[:50]
    
    def research_with_perplexity(self) -> Dict:
        """Use Perplexity API to research the topic"""
        print(f"🔍 Researching '{self.topic}' with Perplexity AI...")
        
        if not PERPLEXITY_API_KEY:
            print("  ⚠️ No Perplexity API key found - using fallback")
            return self.fallback_research()
        
        # Craft a comprehensive research prompt
        prompt = f"""Research the topic "{self.topic}" and provide:

1. A clear, concise explanation of what it is (2-3 sentences)
2. 3-5 key points about how it works or why it's important
3. 1-2 simple analogies that would help an 8-year-old understand it
4. 1-2 real-world examples or applications

Format your response as JSON with these fields:
{{
  "core_concept": "2-3 sentence explanation",
  "key_points": ["point 1", "point 2", ...],
  "analogies": ["analogy 1", "analogy 2"],
  "real_world_examples": ["example 1", "example 2"]
}}"""

        try:
            response = requests.post(
                PERPLEXITY_API_URL,
                headers={
                    "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-sonar-small-128k-online",  # Fast, online model
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a helpful research assistant that provides accurate, well-sourced information in JSON format."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                citations = data.get("citations", [])
                
                # Parse JSON response
                try:
                    # Extract JSON from response (may have markdown formatting)
                    if "```json" in content:
                        content = content.split("```json")[1].split("```")[0].strip()
                    elif "```" in content:
                        content = content.split("```")[1].split("```")[0].strip()
                    
                    research_result = json.loads(content)
                    
                    # Add citations as sources
                    for i, citation in enumerate(citations[:5], 1):
                        self.research_data["sources"].append({
                            "source": "Perplexity",
                            "title": f"Source {i}",
                            "url": citation,
                            "content": ""
                        })
                    
                    # Populate research data
                    self.research_data["core_concept"] = research_result.get("core_concept", "")
                    self.research_data["key_points"] = research_result.get("key_points", [])
                    self.research_data["analogies"] = research_result.get("analogies", [])
                    self.research_data["real_world_examples"] = research_result.get("real_world_examples", [])
                    
                    print(f"  ✅ Found comprehensive research with {len(citations)} sources")
                    return self.research_data
                    
                except json.JSONDecodeError as e:
                    print(f"  ⚠️ Failed to parse JSON response: {e}")
                    # Use raw text as core concept
                    self.research_data["core_concept"] = content[:500]
                    return self.research_data
            else:
                print(f"  ⚠️ API error: {response.status_code} - {response.text}")
                return self.fallback_research()
                
        except Exception as e:
            print(f"  ⚠️ Perplexity API error: {e}")
            return self.fallback_research()
    
    def fallback_research(self) -> Dict:
        """Fallback research using curated knowledge"""
        print("  ℹ️ Using curated fallback research...")
        
        # Curated knowledge base
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
                    "Like a chain of sealed envelopes, where you can't open or change one without everyone noticing"
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
        return self.research_data
    
    def conduct_research(self) -> Dict:
        """Main research workflow"""
        print(f"\n🔬 Starting research for: {self.topic}\n")
        
        # Research with Perplexity
        self.research_with_perplexity()
        
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
        print("Usage: python research_topic_perplexity.py <topic>")
        print("Example: python research_topic_perplexity.py 'quantum computing'")
        sys.exit(1)
    
    topic = ' '.join(sys.argv[1:])
    
    researcher = PerplexityResearcher(topic)
    research_data = researcher.conduct_research()
    
    # Display results
    print("\n" + "="*60)
    print(f"📊 RESEARCH RESULTS: {topic}")
    print("="*60 + "\n")
    
    print(f"Sources found: {len(research_data['sources'])}")
    for source in research_data['sources']:
        print(f"  - {source['source']}: {source.get('url', source.get('title', 'N/A'))}")
    
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
