"""
InnovLead Content Engine - Topic Discovery
Discovers trending tech topics from multiple sources for content creation.

Per directive: directives/discover_topics.md
"""

import os
import sys
import json

# Fix Unicode encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

import requests
from datetime import datetime
from typing import List, Dict
from pathlib import Path

# Configuration
OUTPUT_DIR = Path(".tmp")
OUTPUT_FILE = OUTPUT_DIR / "trending_topics.json"
MAX_TOPICS = 20  # Total topics to discover
MIN_SCORE = 5    # Minimum relevance score (0-10)

# API endpoints
GITHUB_TRENDING_URL = "https://api.github.com/search/repositories"
HACKERNEWS_API = "https://hacker-news.firebaseio.com/v0"


class TopicDiscovery:
    def __init__(self):
        self.topics = []
        self.github_token = os.getenv("GITHUB_TOKEN", "")
        
    def fetch_github_trending(self) -> List[Dict]:
        """Fetch trending repositories from GitHub API"""
        print("🔍 Fetching GitHub trending topics...")
        
        # Tech-related topics to search
        tech_keywords = [
            "artificial intelligence", "machine learning", "blockchain",
            "quantum computing", "cybersecurity", "web3", "docker",
            "kubernetes", "rust programming", "typescript"
        ]
        
        headers = {}
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
        
        topics = []
        
        for keyword in tech_keywords[:3]:  # Limit to avoid rate limits
            try:
                params = {
                    "q": f"{keyword} created:>2025-12-01",
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 5
                }
                
                response = requests.get(
                    GITHUB_TRENDING_URL,
                    params=params,
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    for repo in data.get("items", [])[:2]:  # Top 2 per keyword
                        topics.append({
                            "title": repo["name"],
                            "description": repo.get("description", ""),
                            "source": "GitHub",
                            "url": repo["html_url"],
                            "stars": repo["stargazers_count"],
                            "score": min(10, repo["stargazers_count"] // 100)  # Simple scoring
                        })
                        
            except Exception as e:
                print(f"  ⚠️ Error fetching GitHub data for '{keyword}': {e}")
                
        print(f"  ✅ Found {len(topics)} GitHub topics")
        return topics
    
    def fetch_hackernews_trending(self) -> List[Dict]:
        """Fetch trending stories from Hacker News"""
        print("🔍 Fetching Hacker News trending topics...")
        
        topics = []
        
        try:
            # Get top stories
            response = requests.get(
                f"{HACKERNEWS_API}/topstories.json",
                timeout=10
            )
            
            if response.status_code == 200:
                story_ids = response.json()[:15]  # Top 15 stories
                
                for story_id in story_ids:
                    try:
                        story_response = requests.get(
                            f"{HACKERNEWS_API}/item/{story_id}.json",
                            timeout=5
                        )
                        
                        if story_response.status_code == 200:
                            story = story_response.json()
                            
                            # Filter for tech-related content
                            title = story.get("title", "").lower()
                            if any(kw in title for kw in ["ai", "ml", "blockchain", "quantum", "programming", "tech", "computing", "crypto", "web3"]):
                                topics.append({
                                    "title": story.get("title", ""),
                                    "description": story.get("text", "")[:200] if story.get("text") else "",
                                    "source": "HackerNews",
                                    "url": story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                                    "score": min(10, story.get("score", 0) // 50)  # HN points scoring
                                })
                                
                    except Exception as e:
                        print(f"  ⚠️ Error fetching story {story_id}: {e}")
                        
        except Exception as e:
            print(f"  ⚠️ Error fetching HackerNews data: {e}")
            
        print(f"  ✅ Found {len(topics)} HackerNews topics")
        return topics
    
    def add_curated_topics(self) -> List[Dict]:
        """Add curated evergreen tech topics"""
        print("📚 Adding curated evergreen topics...")
        
        curated = [
            {
                "title": "How Neural Networks Learn",
                "description": "Understanding backpropagation and gradient descent in deep learning",
                "source": "Curated",
                "url": "",
                "score": 8
            },
            {
                "title": "Blockchain Consensus Mechanisms",
                "description": "Proof of Work vs Proof of Stake explained",
                "source": "Curated",
                "url": "",
                "score": 8
            },
            {
                "title": "How Quantum Computers Work",
                "description": "Qubits, superposition, and quantum entanglement explained",
                "source": "Curated",
                "url": "",
                "score": 9
            },
            {
                "title": "Docker Containers Explained",
                "description": "How containerization works and why it matters",
                "source": "Curated",
                "url": "",
                "score": 7
            },
            {
                "title": "Public Key Cryptography",
                "description": "How encryption keeps your data safe online",
                "source": "Curated",
                "url": "",
                "score": 8
            }
        ]
        
        print(f"  ✅ Added {len(curated)} curated topics")
        return curated
    
    def deduplicate_and_score(self, all_topics: List[Dict]) -> List[Dict]:
        """Remove duplicates and rank by score"""
        print("🔄 Deduplicating and scoring topics...")
        
        # Simple deduplication by title similarity
        unique_topics = {}
        for topic in all_topics:
            title_key = topic["title"].lower()[:50]  # First 50 chars
            if title_key not in unique_topics:
                unique_topics[title_key] = topic
            else:
                # Keep higher scored version
                if topic["score"] > unique_topics[title_key]["score"]:
                    unique_topics[title_key] = topic
        
        # Sort by score
        sorted_topics = sorted(
            unique_topics.values(),
            key=lambda x: x["score"],
            reverse=True
        )
        
        # Filter by minimum score
        filtered = [t for t in sorted_topics if t["score"] >= MIN_SCORE]
        
        print(f"  ✅ {len(filtered)} unique topics after deduplication")
        return filtered[:MAX_TOPICS]
    
    def discover_topics(self) -> List[Dict]:
        """Main discovery workflow"""
        print("\n🚀 Starting topic discovery...\n")
        
        # Gather from all sources
        github_topics = self.fetch_github_trending()
        hn_topics = self.fetch_hackernews_trending()
        curated_topics = self.add_curated_topics()
        
        # Combine all sources
        all_topics = github_topics + hn_topics + curated_topics
        
        # Deduplicate and score
        final_topics = self.deduplicate_and_score(all_topics)
        
        return final_topics
    
    def save_topics(self, topics: List[Dict]):
        """Save discovered topics to JSON file"""
        OUTPUT_DIR.mkdir(exist_ok=True)
        
        output_data = {
            "discovered_at": datetime.now().isoformat(),
            "total_topics": len(topics),
            "topics": topics
        }
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Saved {len(topics)} topics to {OUTPUT_FILE}")


def main():
    """Run topic discovery"""
    discovery = TopicDiscovery()
    topics = discovery.discover_topics()
    
    # Display results
    print("\n" + "="*60)
    print(f"📊 DISCOVERED {len(topics)} TECH TOPICS")
    print("="*60 + "\n")
    
    for i, topic in enumerate(topics[:10], 1):  # Show top 10
        print(f"{i}. [{topic['score']}/10] {topic['title']}")
        print(f"   Source: {topic['source']}")
        if topic['description']:
            print(f"   {topic['description'][:80]}...")
        print()
    
    # Save to file
    discovery.save_topics(topics)
    
    print(f"\n✅ Topic discovery complete!")
    print(f"📂 View full results at: {OUTPUT_FILE.absolute()}")


if __name__ == "__main__":
    main()
