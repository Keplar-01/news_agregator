import datetime
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config.database import Session
from services.parser_service import ParserService

from config.logs import jobs_logger

service = ParserService(Session())

async def fetch_news_job():
    jobs_logger.info(f'Команда запущена по расписанию в {datetime.time}: fetch_news_job')
    a = await service.fetch_news_from_url_rss()
    return a

