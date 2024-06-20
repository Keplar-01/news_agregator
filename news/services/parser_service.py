import logging
from datetime import datetime
from typing import List
from dateutil.parser import parse
from sqlalchemy.ext.asyncio import AsyncSession
import aiohttp
from bs4 import BeautifulSoup
import feedparser
import asyncio
from repositories.parse_data_repository import ParseDataRepository
from schemas import parse_data_schema as _schema_parse_data
from schemas import news_schema as _schema_news

from repositories.news_repository import NewsRepository

from config.logs import parser_logger as jobs_logger

from services.producer_service import Producer, producer

INTERVAL = 60

class ParserService():
    def __init__(self, session: AsyncSession):
        self.repository = ParseDataRepository(session)
        self._repository_news = NewsRepository(session)

    async def create(self, parse_data: _schema_parse_data.ParseDataInput) -> _schema_parse_data.ParseDataOutput | None:
        is_exists = await self.repository.get_by_url_list(parse_data.url_list)
        if is_exists is None:
            return await self.repository.create(parse_data)
        return None

    async def get_all(self) -> List[_schema_parse_data.ParseDataOutput]:
        return await self.repository.get_all()

    async def get_by_id(self, parse_data_id: int) -> _schema_parse_data.ParseDataOutput:
        return await self.repository.get_by_id(parse_data_id)

    async def update(self, parse_data_id: int, data: _schema_parse_data.ParseDataInput) -> dict:
        db_parse_data = await self.repository.get_by_id(parse_data_id)

        if not db_parse_data:
            return {"success": False, "result": "Запись не найдена"}

        is_valid = await self.repository.get_by_url_list(data.url_list)

        if is_valid is not None and is_valid.id != parse_data_id:
            return {"success": False, "result": "Запись с таким url уже существует"}

        db_parse_data = await self.repository.update(db_parse_data, data)

        result = _schema_parse_data.ParseDataOutput.from_orm(db_parse_data)

        return {"success": True, "result": result}

    async def delete(self, parse_data_id: int) -> bool:
        parse_data = await self.repository.get_by_id(parse_data_id)
        if not parse_data:
            return False
        return await self.repository.delete(parse_data)

    async def fetch_news_from_url_rss(self):
        jobs_logger.info('Запуск парсера')
        parse_data = await self.repository.get_all()

        try:
            async with aiohttp.ClientSession() as session:
                tasks = []
                for parse in parse_data:
                    jobs_logger.info(f'{parse_data}')
                    task = asyncio.create_task(self._get_news_urls(session, parse.url_list, parse))
                    tasks.append(task)
                await asyncio.gather(*tasks)

        except Exception as e:
            jobs_logger.error(f'Ошибка при получении данных\n{e}\n')
            return False
        return True

    async def _get_news_urls(self, session, url, parse_data):
        if parse_data.type_url == 'html':
            return

        try:
            jobs_logger.info(f'Получаем фид по url: {url}')
            feed = feedparser.parse(url)
            jobs_logger.info(f'Пришло новостей: {len(feed.entries)}')

            tasks = [
                self.process_feed_entry(session, entry, parse_data) for entry in feed.entries
            ]
            await asyncio.gather(*tasks)

        except Exception as e:
            jobs_logger.error(f'Ошибка при получении данных\n{e}\n')
            return False

    async def process_feed_entry(self, session, entry, parse_data):
        try:
            is_new_news = await self._repository_news.get_by_url(entry.link) is None
            if is_new_news:
                async with asyncio.Semaphore(100):
                    jobs_logger.info(f'Текст начинает собираться')
                    await self.get_page_data(session, entry, parse_data.html_tag_element,
                                             parse_data.html_attr_element_type,
                                             parse_data.html_attr_element_value,
                                             parse_data.name, parse_data.id)
        except Exception as e:
            jobs_logger.error(f'Ошибка при обработке записи фида\n{e}\n')

    async def get_page_data(self, session, entry,
                            html_tag, html_attr_type, html_attr_val,
                            source_name, parse_data_id):
        try:
            async with session.get(url=entry.link) as response:
                response_text = await response.text()
        except Exception as e:
            jobs_logger.error(f'Error while getting page data: {e}')
            return False

        soup = BeautifulSoup(response_text, 'lxml')
        texts = soup.find_all(html_tag, {html_attr_type: html_attr_val})
        summary_text = " ".join(text.get_text().strip() for text in texts)
        date = parse(entry.published)

        new_model = _schema_news.NewsInput(
            text=summary_text,
            url=entry.link,
            date=date,
            title=entry.title,
            name_source=source_name,
            is_train=False,
            parse_data_id=parse_data_id,
            mood=""
        )

        try:
            news = await self._repository_news.create(new_model)
            jobs_logger.info(f'Обработана новость')
        except Exception as e:
            jobs_logger.error(f'Error while inserting into database: {e}')
            return False

        try:
            await producer.send({"text_id": news.id, "text": news.text, "correlation_id": str(news.id)})
        except Exception as e:
            jobs_logger.error(f'Error while sending message to queue: {e}')
            return False

        return True
