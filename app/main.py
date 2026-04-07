from fastapi import FastAPI
from pydantic import BaseModel
from app.services.scraper import scrape_website
from app.services.ai_handler import summarize_text
import csv
import os
from datetime import datetime

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str

def save_to_history(data):
    file_exists = os.path.isfile("news_history.csv")

    with open("news_history.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Date", "Title", "Sentiment", "Score", "URL"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data["title"],
            data.get("sentiment", "N/A"),
            data.get("sentiment_score", 0),
            data.get("url", "N/A")
        ])

@app.post("/api/process")
def processnews(request: ScrapeRequest):
    # scrape
    scrape_data = scrape_website(request.url)

    if "error" in scrape_data:
        return scrape_data
    
    # AI Summarize
    ai_summary = summarize_text(scrape_data["content"])

    # conbien and return
    result = {
        "title": scrape_data["title"],
        "summary": ai_summary.get("summary"),
        "keywords": ai_summary.get("keywords"),
        "sentiment": ai_summary.get("sentiment"),
        "sentiment_score": ai_summary.get("sentiment_score"),
        "full_text_preview": scrape_data["content"][:200] + "...",
        "url": request.url,
        "main_image": scrape_data.get("main_image")
    }

    save_to_history(result)
    return result