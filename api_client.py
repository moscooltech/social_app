"""
API Client for multiple AI providers
Supports: Gemini, Groq, OpenRouter, Bytez
"""

import requests
import json
from storage import StorageManager


class APIClient:
    """Unified API client for all AI providers"""
    
    def __init__(self):
        self.storage = StorageManager()
        self.api_keys = self.storage.get_api_keys()
    
    def refresh_keys(self):
        """Refresh API keys from storage"""
        self.api_keys = self.storage.get_api_keys()
    
    def generate_text(self, prompt, platform='General', tone='Professional'):
        """
        Generate text content using available AI providers
        Priority: Groq (fastest) -> Gemini -> OpenRouter
        """
        self.refresh_keys()
        
        # Build enhanced prompt
        enhanced_prompt = self._build_prompt(prompt, platform, tone)
        
        # Try providers in order of preference
        providers = [
            ('groq', self._generate_with_groq),
            ('gemini', self._generate_with_gemini),
            ('openrouter', self._generate_with_openrouter),
        ]
        
        for provider_name, provider_func in providers:
            if self.api_keys.get(provider_name):
                try:
                    return provider_func(enhanced_prompt)
                except Exception as e:
                    print(f"{provider_name} failed: {e}")
                    continue
        
        raise Exception("No API keys configured or all providers failed. Please add API keys in Settings.")
    
    def generate_image(self, prompt):
        """Generate image using Bytez API"""
        self.refresh_keys()
        
        bytez_key = self.api_keys.get('bytez')
        if not bytez_key:
            raise Exception("Bytez API key not configured")
        
        return self._generate_with_bytez(prompt)
    
    def _build_prompt(self, user_prompt, platform, tone):
        """Build enhanced prompt with platform and tone context"""
        platform_instructions = {
            'Twitter': 'Create a concise, engaging tweet (max 280 characters). Use emojis strategically.',
            'LinkedIn': 'Write a professional post suitable for LinkedIn. Focus on value and insights.',
            'Instagram': 'Create an engaging caption perfect for Instagram. Use relevant hashtags.',
            'Facebook': 'Write a friendly, shareable Facebook post that encourages engagement.',
            'General': 'Create engaging social media content.'
        }
        
        tone_instructions = {
            'Professional': 'Use a professional, polished tone.',
            'Casual': 'Write in a casual, conversational style.',
            'Enthusiastic': 'Be energetic and enthusiastic!',
            'Formal': 'Maintain a formal, authoritative tone.',
            'Funny': 'Make it humorous and entertaining.',
            'Inspirational': 'Be motivational and uplifting.'
        }
        
        platform_inst = platform_instructions.get(platform, platform_instructions['General'])
        tone_inst = tone_instructions.get(tone, '')
        
        return f"""{platform_inst} {tone_inst}

Topic: {user_prompt}

Generate the content now:"""
    
    def _generate_with_groq(self, prompt):
        """Generate text using Groq API (fastest)"""
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_keys['groq']}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.3-70b-versatile",  # Fast and good quality
            "messages": [
                {"role": "system", "content": "You are a professional social media content creator."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    
    def _generate_with_gemini(self, prompt):
        """Generate text using Google Gemini API"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_keys['gemini']}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 500
            }
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text'].strip()
    
    def _generate_with_openrouter(self, prompt):
        """Generate text using OpenRouter API"""
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_keys['openrouter']}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "google/gemini-2.0-flash-exp:free",  # Free model
            "messages": [
                {"role": "system", "content": "You are a professional social media content creator."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    
    def _generate_with_bytez(self, prompt):
        """Generate image using Bytez API"""
        url = "https://api.bytez.com/v1/image/generate"
        headers = {
            "Authorization": f"Bearer {self.api_keys['bytez']}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt,
            "model": "flux-schnell",  # Fast and free
            "width": 1024,
            "height": 1024
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        # Return the image URL
        return result.get('data', {}).get('url') or result.get('url') or 'Image generated (check API response format)'
