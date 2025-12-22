import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def ask_llm(question: str) -> str:
    try:
        payload = {
            "model": MODEL,
            "prompt": question,
            "stream": False
        }

        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()

        return response.json().get("response", "No response generated.")

    except Exception as e:
        return (
            "I couldn't generate an AI-based explanation for this question. "
            "However, forecasting and historical analysis are still available."
        )
