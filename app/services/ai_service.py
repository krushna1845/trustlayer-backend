from anthropic import Anthropic
from app.config import settings
from typing import Dict, Any, List
import json

class AIService:
    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    async def analyze_contract(self, contract_text: str) -> Dict[str, Any]:
        """Analyze contract using Claude AI"""
        
        prompt = f"""Analyze the following contract and provide a detailed analysis in JSON format with the following structure:

{{
  "summary": "Brief summary of the contract",
  "key_terms": [
    {{"term": "Term name", "definition": "Definition", "importance": "high/medium/low"}}
  ],
  "risk_score": 0-100,
  "risks": [
    {{"risk": "Risk description", "severity": "high/medium/low", "mitigation": "Suggested mitigation"}}
  ],
  "recommendations": ["List of recommendations"],
  "clauses": [
    {{"clause_name": "Name", "description": "Description", "page": 1}}
  ],
  "parties_involved": ["List of parties"],
  "obligations": [
    {{"party": "Party name", "obligation": "Obligation description", "deadline": "Deadline if any"}}
  ]
}}

Contract Text:
{contract_text}

Provide ONLY the JSON response, no additional text."""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.content[0].text
            
            # Parse JSON response
            try:
                analysis = json.loads(content)
                return analysis
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract JSON from markdown
                if "```json" in content:
                    json_str = content.split("```json")[1].split("```")[0].strip()
                    return json.loads(json_str)
                else:
                    return {"error": "Failed to parse AI response", "raw_response": content}
        
        except Exception as e:
            return {"error": str(e)}
    
    async def chat_about_contract(self, contract_text: str, user_message: str, chat_history: List[Dict] = None) -> str:
        """Chat with AI about a specific contract"""
        
        messages = []
        
        # Add system context
        system_message = f"""You are a legal AI assistant helping users understand their contracts. 
Here is the contract being discussed:

{contract_text[:3000]}...

Answer questions about this contract clearly and helpfully."""
        
        # Add chat history if exists
        if chat_history:
            for msg in chat_history[-5:]:  # Last 5 messages for context
                messages.append({"role": "user", "content": msg.get("message", "")})
                if msg.get("response"):
                    messages.append({"role": "assistant", "content": msg.get("response", "")})
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                system=system_message,
                messages=messages
            )
            
            return response.content[0].text
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def assess_risk(self, contract_text: str) -> Dict[str, Any]:
        """Quick risk assessment"""
        
        prompt = f"""Provide a quick risk assessment for this contract in JSON format:

{{
  "overall_risk_score": 0-100,
  "risk_level": "low/medium/high/critical",
  "top_risks": [
    {{"risk": "Description", "severity": "high/medium/low"}}
  ],
  "red_flags": ["List of immediate concerns"],
  "safe_aspects": ["List of positive aspects"]
}}

Contract:
{contract_text}

Provide ONLY JSON, no additional text."""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                if "```json" in content:
                    json_str = content.split("```json")[1].split("```")[0].strip()
                    return json.loads(json_str)
                return {"error": "Failed to parse response"}
        
        except Exception as e:
            return {"error": str(e)}
