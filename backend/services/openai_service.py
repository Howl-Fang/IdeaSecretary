import requests
import json
from typing import Optional, Dict, Any
from datetime import datetime

class OpenAIClient:
    """Client for OpenAI API integration"""
    
    def __init__(self, api_key: str, api_url: str = 'https://api.openai.com/v1', model: str = 'gpt-3.5-turbo'):
        self.api_key = api_key
        self.api_url = api_url.rstrip('/')
        self.model = model
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def organize_idea(self, content: str, title: str) -> Optional[str]:
        """Get AI suggestions for organizing an idea"""
        prompt = f"""Please analyze the following idea and provide structured suggestions for organizing and categorizing it.

Title: {title}
Content: {content}

Provide your response in JSON format with:
- suggested_tags: list of 3-5 relevant tags
- category: main category suggestion
- summary: brief summary
- insights: key insights or interesting aspects
- related_topics: potential related topics to explore"""
        
        return self._call_api(prompt, system_prompt=self._get_system_prompt())
    
    def generate_inspiration(self, existing_ideas: list) -> Optional[str]:
        """Generate inspirations based on existing ideas"""
        ideas_text = '\n'.join([f"- {idea}" for idea in existing_ideas[:10]])
        
        prompt = f"""Based on these existing ideas:
{ideas_text}

Please suggest 3-5 related ideas or topics to explore next. Return as JSON with:
- suggestions: list of idea suggestions
- connections: potential connections between ideas"""
        
        return self._call_api(prompt, system_prompt=self._get_system_prompt())
    
    def summarize_ideas(self, ideas: list) -> Optional[str]:
        """Summarize multiple ideas"""
        ideas_text = '\n'.join([f"- {idea}" for idea in ideas])
        
        prompt = f"""Please summarize these ideas and identify common themes:
{ideas_text}

Return as JSON with:
- summary: overall summary
- themes: common themes
- key_points: key takeaways"""
        
        return self._call_api(prompt, system_prompt=self._get_system_prompt())
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for AI"""
        return """You are an expert knowledge organizer and idea structurer. Your role is to:
1. Help users organize and categorize their ideas
2. Identify relationships between different thoughts
3. Provide actionable insights
4. Suggest related topics to explore

Always respond in valid JSON format when requested. Be concise and focus on clarity."""
    
    def _call_api(self, prompt: str, system_prompt: str = None) -> Optional[str]:
        """Call OpenAI API"""
        try:
            messages = []
            
            if system_prompt:
                messages.append({
                    'role': 'system',
                    'content': system_prompt
                })
            
            messages.append({
                'role': 'user',
                'content': prompt
            })
            
            payload = {
                'model': self.model,
                'messages': messages,
                'temperature': 0.7,
                'max_tokens': 1500
            }
            
            response = requests.post(
                f'{self.api_url}/chat/completions',
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'choices' in data and len(data['choices']) > 0:
                    return data['choices'][0]['message']['content']
            
            return None
            
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            return None
