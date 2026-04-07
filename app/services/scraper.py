import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_website(url: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract Title and Text
        title = soup.title.string if soup.title else "No Title"
        paragraphs = soup.find_all('p')
        text_content = " ".join([p.get_text() for p in paragraphs])

        # --- NEW IMAGE EXTRACTION LOGIC ---
        main_image_url = None

        # Strategy 1: Look for the official Open Graph (og:image) meta tag
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            main_image_url = og_image.get("content")

        # Strategy 2: Fallback to searching <img> tags, but STOP after the first valid one
        if not main_image_url:
            bad_keywords = ['logo', 'icon', 'appstore', 'googleplay', 'banner', 'button', 'promo', 'avatar']
            
            for img in soup.find_all('img'):
                src = img.get('src') or img.get('data-src') 
                
                if src:
                    absolute_url = urljoin(url, src)
                    url_lower = absolute_url.lower()

                    if url_lower.endswith('.svg') or "tr?id=" in url_lower:
                        continue
                    if any(bad_word in url_lower for bad_word in bad_keywords):
                        continue
                    if not url_lower.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                         continue

                    # We found the first valid image! 
                    main_image_url = absolute_url
                    break # <-- This immediately stops the loop so we don't grab related articles

        return {
            "title": title,
            "content": text_content[:3000],
            "main_image": main_image_url # Notice this is now a single string, not a list
        }
        
    except Exception as e:
        return {"error" : str(e)}