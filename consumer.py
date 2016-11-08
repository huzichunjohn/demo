import logging

from celery import Celery
from celery import bootsteps

from django.conf import settings
from kombu import Consumer, Exchange, Queue

from indexer import tasks

exchange = Exchange(settings.EVENT_EXCHANGE, type='topic')

content_ingestion_queue = Queue(settings.CONTENT_INGESTION_QUEUE, exchange=exchange, routing_key=settings.CONTENT_ROUTING_KEY)

app = Celery('consumers', broker=settings.EVENT_BROKER)
log = logging.getLogger(__name__)

class IngestionConsumerStep(bootsteps.ConsumeStep):
    def get_consumers(self, channel):
	return [Consumer(channel,
			 queues=[content_ingestion_queue],
			 callbacks=[self.handle_message],
			 accept=['json'])]

    def handle_message(self, body, message):
	log.info("Received content update message: {0!r}".format(body)
	if 'identifier' in body:
	    tasks.index_book.delay(body['identifier'])
	else:
	    log.warn("Ignored content update message because it lacked an identifier")
	message.ack()

app.steps['consumer'].add(IngestionConsumerStep)
