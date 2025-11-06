from fastapi import FastAPI, Request
import requests, os, json
from utils.parser import parse_ai_response
import logging
logging.basicConfig(level=logging.INFO)
if os.getenv("OPENROUTER_API_KEY") is None: 
    from dotenv import load_dotenv
    load_dotenv()


app = FastAPI()

@app.post("/prompt")
async def handle_prompt(request: Request):
    data = await request.json()
    user_input = data.get("text", "")
    logging.info(f"User input: {user_input}")
    logging.info(f"OpenRouter key present: {bool(os.getenv('OPENROUTER_API_KEY'))}")

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "user",
                "content": (
                    "You are a parser. Extract information from the user command below.\n\n"
                    f"Input: {user_input}\n\n"
                    "Return ONLY valid JSON with the following exact keys:\n"
                    "{\n"
                    "  'action': string or null,   # what needs to be done (e.g., 'call', 'text', 'voicemail')\n"
                    "  'number': string or null,   # phone number if provided\n"
                    "  'command': string or null  # the message or instruction to deliver in first person active voice, null if not given\n"
                    "}\n"
                    "No extra text, explanations, or formatting outside JSON."
                )
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=10
        )
        response.raise_for_status() 
        llm_text = response.json()["choices"][0]["message"]["content"]
        logging.info(f"Raw LLM output: {llm_text}")
    except Exception as e:
        print(f"OpenRouter error: {e}")
        llm_text = json.dumps({
            "action": None,
            "number": None,
            "command": None,
        })

    parsed = parse_ai_response(llm_text)
    return parsed
