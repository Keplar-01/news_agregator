import aio_pika
import json
import asyncio

class Producer:
    def __init__(self, loop, queue_name, send_function):
        self.loop = loop
        self.queue_name = queue_name
        self.send_function = send_function

    async def connect(self):
        self.connection = await aio_pika.connect_robust("amqp://rabbitmq/", loop=self.loop)
        self.channel = await self.connection.channel()
        await self.channel.declare_queue(self.queue_name, durable=True)

    async def send(self, message):
        if self.send_function:
            await self.send_function(self, message)


async def send_message_classification(self, message):
    if message['text_id'] is None or message['text'] is None:
        return
    correlation_id = message['correlation_id']
    del message['correlation_id']
    await self.channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(message).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            correlation_id=correlation_id,
            reply_to=self.queue_name
        ),
        routing_key=self.queue_name
    )
    print(" [x] Sent %r" % message)


async def send_message_control(self, message):
    await self.channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(message).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            correlation_id=message['correlation_id'],
            reply_to=self.queue_name
        ),
        routing_key=self.queue_name
    )
    print(f" [x] Sent {message}")

loop = asyncio.get_event_loop()
producer = Producer(loop, 'classification_queue', send_message_classification)

producer_contol = Producer(loop, 'control_queue', send_message_control)