
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from jobs.fetch_news import fetch_news_job

scheduler = AsyncIOScheduler()

scheduler.add_job(fetch_news_job, 'interval', minutes=15)