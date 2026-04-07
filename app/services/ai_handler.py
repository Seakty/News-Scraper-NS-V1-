from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv() # Load environment variables from .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text_content):
    try:
        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            response_format = {"type": "json_object"},
            messages = [
                {
                    "role": "system", "content": """
                    You are a News Analyst.
                    YOu must return a JSON object with these key:
                    1. "summary": A concise summary (Max 3 sentences).
                    2. "keywords": A list of 3-5 key topics. 
                    3. "sentiment": one of ["positive", "negative", "neutral"] based on the overall tone of the text.
                    4. "sentiment_score": An interger from 0 (Negative) to 100 (Positive) representing the strength of the sentiment.
                    """
                },
                {
                    "role": "user", "content": f"Analyze this text: {text_content}"
                }
            ]

        )
        return json.loads(response.choices[0].message.content)
    
    except Exception as e:
        return {"error": str(e)}

    