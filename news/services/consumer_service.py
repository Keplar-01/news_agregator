import asyncio
import threading

import pika
import json

from config.database import Session
from services.news_service import NewsService
from schemas import news_schema as _schema

from repositories.classes_repository import ClassesRepository

print('consumer')
class Consumer:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.news_service = NewsService(Session())
        self.clases_repository = ClassesRepository(Session())

    def callback(self, ch, method, properties, body):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.async_callback(ch, method, properties, body))
        loop.close()

    async def async_callback(self, ch, method, properties, body):
        data = json.loads(body)
        text_id = data['text_id']
        text_class = data['text_class']
        text_mood = data['text_mood']

        news = await self.news_service.get_by_id(text_id)
        if news:
            classes = await self.clases_repository.get_by_name(text_class)

            news_dict = {key: value for key, value in news.__dict__.items() if not key.startswith('_')}
            news_dict['classes_id'] = classes.id
            news_dict['mood'] = text_mood

            news_input = _schema.NewsInput(**news_dict)
            data = await self.news_service.update(news.id, news_input)
            print('ОБНОВИЛ')
        else:
            print('Новость не найдена')

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=False)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()


def start_consumer():
    consumer = Consumer('classification_queue_answer')
    thread = threading.Thread(target=consumer.start_consuming)
    thread.start()