import json
from fastapi import HTTPException, Query, APIRouter
from typing import List
import asyncio
import httpx
from app.core.cache import get_cache, set_cache
from app.core.config import settings

router = APIRouter()

async def fetch_news_for_category(category: str):
    cache_key = f"news:{category}"
    cached_data = await get_cache(cache_key)
    
    if cached_data:
        return json.loads(cached_data)

    url = f"https://newsapi.org/v2/top-headlines"
    params = {
        "category": category,
        "apiKey": settings.NEWS_API_KEY,
        "country": "india",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching news")

        news_data = response.json()
        if news_data["status"] != "ok":
            raise HTTPException(status_code=500, detail="Error with the news API")

        articles = news_data["articles"]
        await set_cache(cache_key, json.dumps(articles))
        
        return articles

async def fetch_all_news(categories: List[str]):
    tasks = [fetch_news_for_category(category) for category in categories]
    news_by_category = await asyncio.gather(*tasks)
    
    return [article for news in news_by_category for article in news]

@router.get("/news")
async def get_news(categories: List[str] = Query(default=["technology", "business"], description="List of news categories")):
    try:
        news_data = await fetch_all_news(categories)
        return news_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))