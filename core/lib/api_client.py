"""
Shared API Client for Antigravity Platform
Handles authentication, rate limiting, error handling for all modules
"""

import os
import time
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class APIClient:
    """Reusable API client with built-in error handling and rate limiting"""
    
    def __init__(self, base_url: str, api_key: str = None, rate_limit: float = 0.5):
        self.base_url = base_url
        self.api_key = api_key
        self.rate_limit = rate_limit  # Seconds between requests
        self.last_request_time = 0
    
    def _wait_for_rate_limit(self):
        """Ensure we don't exceed rate limits"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request_time = time.time()
    
    def get(self, endpoint: str, params: Dict = None, headers: Dict = None) -> Dict:
        """GET request with error handling"""
        self._wait_for_rate_limit()
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        _headers = self._build_headers(headers)
        
        try:
            response = requests.get(url, params=params, headers=_headers, timeout=30)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def post(self, endpoint: str, data: Dict = None, headers: Dict = None) -> Dict:
        """POST request with error handling"""
        self._wait_for_rate_limit()
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        _headers = self._build_headers(headers)
        
        try:
            response = requests.post(url, json=data, headers=_headers, timeout=30)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def _build_headers(self, custom_headers: Dict = None) -> Dict:
        """Build headers with API key if available"""
        headers = {"Content-Type": "application/json"}
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        if custom_headers:
            headers.update(custom_headers)
        
        return headers


# Pre-configured clients for common APIs
def get_gemini_client() -> APIClient:
    """Get configured Gemini API client"""
    api_key = os.getenv("GEMINI_API_KEY")
    return APIClient(
        base_url="https://generativelanguage.googleapis.com/v1beta",
        api_key=api_key,
        rate_limit=1.0  # 60/min = ~1/sec
    )


def get_keiai_client() -> APIClient:
    """Get configured Kei.ai API client"""
    api_key = os.getenv("KEI_AI_API_KEY")
    return APIClient(
        base_url="https://api.kie.ai/api/v1",
        api_key=api_key,
        rate_limit=0.5
    )



