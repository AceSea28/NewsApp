# Defines API routes and logic for news-related operations.

from fastapi import FastAPI, HTTPException, Query, APIRouter
from typing import List
import asyncio
import httpx

router = APIRouter()

async def fetch_news_for_category(category: str):
    try:
        # Example API URL. Replace with the actual news API URL.
        url = f"https://newsapi.org/v2/top-headlines?country=us&language=en&category={category}&apiKey=dba9e44376bd4f62ab7d5710bd62f238"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            
            # Assuming the API returns a JSON response with a list of articles.
            news_data = response.json().get("articles", [])
            filtered_articles = [
                {"title": article.get("title")
                #  , "description": article.get("description")
                } 
                for article in news_data
                ]
            return filtered_articles
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def fetch_all_news(categories: List[str]):
    try:
        tasks = [fetch_news_for_category(category) for category in categories]
        news_by_category = await asyncio.gather(*tasks)
        # Flatten the list of lists into a single list of articles
        news_data = [article for news in news_by_category for article in news]
        
        return news_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/news")
async def get_news(categories: List[str] = Query(default=["technology", "business"], description="List of news categories")):
    try:
        news_data = await fetch_all_news(categories)
        return news_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
