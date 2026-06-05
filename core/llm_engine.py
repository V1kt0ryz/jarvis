import ollama
import json
import re
from utils.logger import setup_logger
from config import LLM_MODEL, OLLAMA_HOST

logger = setup_logger(__name__)

class LLMEngine:
    SYSTEM_PROMPT = """
Du bist Jarvis, ein intelligenter KI-Assistent auf Deutsch.

WICHTIGE BEFEHLE:

1. PROGRAMM ÖFFNEN:
{"action":"open_program","program":"discord"}

2. WEBSEITE ÖFFNEN:
{"action":"open_website","url":"https://youtube.com"}

3. GOOGLE SUCHE:
{"action":"search_google","query":"RTX 5090"}

4. SPEICHERN:
{"action":"remember","key":"Name","value":"Wert"}

5. ABRUFEN:
{"action":"recall","key":"Name"}

6. NORMALE UNTERHALTUNG:
{"action":"chat","response":"Hallo!"}

REGELN:
- Antworte IMMER mit genau EINEM JSON-Objekt
- Keine Erklärungen außerhalb des JSON
- Kein Markdown
- Kein Text vor oder nach dem JSON
- Antworte auf Deutsch
"""
    
    def __init__(self):
        self.conversation_history = [
            {"role": "system", "content": self.SYSTEM_PROMPT}
        ]
    
    def process(self, user_input):
        """Process user input and return action"""
        try:
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            response = ollama.chat(
                model=LLM_MODEL,
                messages=self.conversation_history,
                stream=False
            )
            
            answer = response["message"]["content"]
            data = self._parse_response(answer)
            
            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": json.dumps(data, ensure_ascii=False)
            })
            
            return data
        except Exception as e:
            logger.error(f"LLM Error: {e}")
            return {"action": "chat", "response": f"Fehler: {e}"}
    
    def _parse_response(self, response_text):
        """Extract JSON from response"""
        try:
            response_text = response_text.replace("```json", "").replace("```", "").strip()
            match = re.search(r"\{.*\}", response_text, re.DOTALL)
            
            if match:
                data = json.loads(match.group())
                return data
            else:
                return {"action": "chat", "response": response_text}
        except json.JSONDecodeError:
            return {"action": "chat", "response": response_text}
        except Exception as e:
            logger.error(f"Parse error: {e}")
            return {"action": "chat", "response": "Parsing error"}