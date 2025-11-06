from fastapi import FastAPI, Request
import requests, os, json, logging
from utils.parser import ContentItem, PersonalizedContent
from typing import List

logging.basicConfig(level=logging.INFO)

if os.getenv("OPENROUTER_API_KEY") is None:
    from dotenv import load_dotenv
    load_dotenv()

app = FastAPI()

@app.post("/personalizedcontent")
async def handle_prompt(request: Request):
    try:
        data = await request.json()
        user_inputs: List[ContentItem] = [ContentItem(**item) for item in data.get("items", [])]
    except Exception as e:
        logging.error(f"Invalid input format: {e}")
        return {"error": "Invalid JSON input structure"}

    results = []
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
    }

    for item in user_inputs:
        logging.info(f"Processing: {item.title} ({item.word_length} words requested)")

        prompt = (
            f"You are a Professional SEO Optimized Blog Writer, creating personalized content pieces for below topic.\n\n"
            f"Title: {item.title}\n"
            f"Description: {item.description}\n"
            f"Desired Word Count: {item.word_length}\n\n"
            "Write it in an engaging, concise style suitable for a blog post."
        )

        payload = {
            "model": "openai/gpt-oss-20b:free",
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload),
                timeout=20
            )
            response.raise_for_status()
            llm_text = response.json()["choices"][0]["message"]["content"]

            # Calculate actual word count
            word_count = len(llm_text.split())
            logging.info(f"Generated {word_count} words for {item.title}")

            results.append(
                PersonalizedContent(
                    title=item.title,
                    content=llm_text.strip(),
                    word_count_doc=word_count
                ).dict()
            )

        except Exception as e:
            logging.error(f"OpenRouter request failed for {item.title}: {e}")
            results.append(
                PersonalizedContent(
                    title=item.title,
                    content="[Error generating content]",
                    word_count_doc=0
                ).dict()
            )

    return {"results": results}
