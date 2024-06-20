import json
import os
import threading

import pika
import yadisk
import logging

from dotenv import load_dotenv

import ml_service as _ml_service


classification_logger = logging.getLogger('classification_queue')
control_logger = logging.getLogger('control_queue')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
classification_handler = logging.FileHandler('logs/classification.log')
control_handler = logging.FileHandler('logs/control.log')
classification_logger.addHandler(classification_handler)
control_logger.addHandler(control_handler)
load_dotenv()

client = yadisk.Client(token=os.getenv('YANDEX_TOKEN'))
ml_service = _ml_service.MlModelService()
mood_service = _ml_service.MoodModelService()


class Consumer:
    def __init__(self, queue_name, callback):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.callback = callback

    def start_consuming(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=False)
        print(f' [*] Waiting for messages in {self.queue_name}. To exit press CTRL+C')
        self.channel.start_consuming()


def callback_classification(ch, method, properties, body):
    data = json.loads(body)
    text_id = data['text_id']
    text = data['text']

    try:
        text_class = ml_service.predict(text)
        text_mood = mood_service.predict(text)
    except Exception as e:
        classification_logger.error(f'Ошибка при классификации текста {e}')
        ch.basic_ack(delivery_tag = method.delivery_tag)
        return

    classification_logger.info(f'Текст {text_id} - {text_class} - {text_mood}')
    response = {
        'text_id': text_id,
        'text_class': text_class,
        'text_mood': text_mood
    }
    ch.basic_publish(exchange='',
                     routing_key='classification_queue_answer',
                     properties=pika.BasicProperties(correlation_id= \
                                                         properties.correlation_id),
                     body=json.dumps(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

def download_if_not_exists(client, remote_path, local_path, timeout=100000):
    if not os.path.exists(local_path):
        client.download(remote_path, local_path, timeout=timeout)
        control_logger.info(f'Загрузил в {local_path}')

def callback_control(ch, method, properties, body):
    data = json.loads(body)

    command_name = data['command']
    ch.basic_ack(delivery_tag=method.delivery_tag)
    if command_name == 'set_model':
        control_logger.info(f'Начало установки модели')
        try:
            download_if_not_exists(client, 'model/' + data['path_model'], 'ml_models/' + data['path_model'])
            download_if_not_exists(client, 'encoder/' + data['path_encoder'],
                                   'ml_models/encoders/' + data['path_encoder'])
            download_if_not_exists(client, 'tokenizer/' + data['path_tokenizer'],
                                   'ml_models/tokenizer/' + data['path_tokenizer'])

            if 'path_sub_model' in data and client.exists('sub_model/' + data['path_sub_model']):
                download_if_not_exists(client, 'sub_model/' + data['path_sub_model'],
                                       'ml_models/w2v_model/' + data['path_sub_model'])
        except Exception as e:
            control_logger.error(f'Ошибка при загрузке модели {e}')
            return

        ml_service.set_model(data['path_model'])
        ml_service.load_encoder(data['path_encoder'])
        ml_service.load_tokenizer(data['path_tokenizer'])

        if 'path_sub_model' in data:
            ml_service.load_w2v_model(data['path_sub_model'])
        control_logger.info(f'Модель {data["path_model"]} установлена')



def start_consumers():
    consumer1 = Consumer('classification_queue', callback_classification)
    consumer2 = Consumer('control_queue', callback_control)
    thread1 = threading.Thread(target=consumer1.start_consuming)
    thread2 = threading.Thread(target=consumer2.start_consuming)
    thread1.start()
    thread2.start()
