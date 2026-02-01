"""
Generate Strategy Script
Uses Gemini to analyze research and propose automation opportunities
"""

import sys
import os
import json
from datetime import datetime

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import requests

class SimpleGemini:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={self.api_key}"
        
    def generate_content(self, prompt):
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        try:
            response = requests.post(self.url, json=payload, headers={'Content-Type': 'application/json'})
            if response.status_code != 200:
                return f"Error: {response.text}"
            
            data = response.json()
            return data['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            return f"Error calling Gemini: {e}"



def generate_strategy(company_name: str, research_data: dict, save_to_file: bool = True):
    """
    Generate strategic automation opportunities based on research
    """
    print(f"[LOGIC] Generating strategy for: {company_name}")
    
    client = SimpleGemini()
    
    # Construct Consultant Prompt
    prompt = f"""
    ROLE: Senior Solutions Architect at InnovLead (AI & Automation Agency).
    GOAL: Analyze research data and identify 3 concrete "Kill Opportunities" to sell automation.
    
    CONTEXT (InnovLead's Toolkit):
    1. n8n Workflows (for process automation, data sync, reporting)
    2. Replit Apps (for custom dashboards, internal tools, customer portals)
    3. AI Agents (for support, research, lead gen)
    4. Content Pipelines (automated social media, video generation)
    
    RESEARCH DATA:
    {json.dumps(research_data, indent=2)}
    
    INSTRUCTIONS:
    1. Scan 'hiring_signals' for manual labor (e.g. data entry -> n8n automation).
    2. Scan 'tech_signals' for messy stacks (e.g. legacy systems -> Replit wrapper).
    3. Scan 'market_signals' for growth pain (e.g. scaling support -> AI Agent).
    
    OUTPUT FORMAT (JSON):
    {{
        "executive_summary": "Direct, punchy 2-sentence hook about why they need to modernize.",
        "analysis_matrix": [
            {{ "signal": "Found job post for Data Entry", "implication": "Burning $40k/yr on manual work", "solution": "n8n pipeline" }}
        ],
        "opportunities": [
            {{
                "title": "Name of the Solution (e.g. 'Autonomous Support Agent')",
                "pain_point": "Why it hurts them now",
                "proposed_solution": "Technical implementation detail (e.g. 'Deploy n8n webhook + Gemini 2.0')",
                "roi_impact": "Estimated Savings/Growth (be specific, e.g. 'Save 20hrs/week')",
                "confidence": "High/Med/Low"
            }}
        ],
        "draft_email": "A cold email to the CTO pitching the #1 opportunity. Short, value-first."
    }}
    """
    
    print("...querying Gemini")
    response = client.generate_content(prompt)
    
    # Parse JSON from response
    try:
        # Strip markdown code blocks if present // TODO: Move to util
        clean_json = response.replace("```json", "").replace("```", "").strip()
        strategy = json.loads(clean_json)
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        strategy = {"raw_response": response}
        
    if save_to_file:
        output_dir = os.path.join(os.path.dirname(__file__), "../.tmp/strategy")
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{company_name.lower().replace(' ', '_')}_strategy.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(strategy, f, indent=2)
            
        print(f"[SUCCESS] Strategy saved to: {filepath}")
        
    return strategy

if __name__ == "__main__":
    # Test mode - requires existing research file
    if len(sys.argv) > 1:
        company = sys.argv[1]
        # Try to load existing research
        path = f"../.tmp/research/{company.lower().replace(' ', '_')}_research.json"
        full_path = os.path.join(os.path.dirname(__file__), path)
        
        if os.path.exists(full_path):
            with open(full_path, 'r') as f:
                data = json.load(f)
            generate_strategy(company, data)
        else:
            print(f"No research found for {company}. Run research_client.py first.")
    else:
        print("Usage: py generate_strategy.py 'Company Name'")
