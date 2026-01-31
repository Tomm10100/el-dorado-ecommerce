"""
Test Image Generation via n8n -> Replit
Triggers the existing 'Image Assistant' workflow in your n8n cloud.
"""

import sys
import os
import requests
import json
from datetime import datetime

# Webhook URL from your architecture
WEBHOOK_URL = "https://innovlead.app.n8n.cloud/webhook/d2de64ab-ce17-4cfc-a53a-c56b0c949b21"

def generate_test_image(prompt="A futuristic city with flying cars, cyberpunk style"):
    print(f"Triggering Image Generation...")
    print(f"Target: {WEBHOOK_URL}")
    print(f"Prompt: {prompt}")
    
    payload = {
        "service_type": "text-to-image",
        "prompt": prompt,
        "aspect_ratio": "16:9",
        "resolution": "1K",
        "output_format": "png",
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            print("[SUCCESS] Workflow triggered.")
            print("Check your Replit App (Finished Images) in a few seconds.")
            print(f"Response: {response.text}")
        else:
            print(f"[FAILED] Failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"[ERROR] Error: {e}")

if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else "A happy robot programmer building a bridge"
    generate_test_image(p)
