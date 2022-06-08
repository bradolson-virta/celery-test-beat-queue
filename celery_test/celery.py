from celery.utils.log import get_task_logger
from os import environ

from celery import Celery, bootsteps, Task
from celery.schedules import crontab
from kombu import Exchange, Queue
from datetime import timedelta

from celery.utils.log import get_task_logger
from celery import group

broker = environ.get('MESSAGE_BROKER_URL', 'amqp://guest:guest@localhost:5672//')
redis = environ.get('REDIS_URL', 'redis://localhost:6379/0')

ACTION_LIST_EVENT_QUEUE = 'action_list_event_queue'

logger = get_task_logger(ACTION_LIST_EVENT_QUEUE)

celery_app = Celery('action_list_event', backend=redis, broker=broker)
celery_config = {
    'task_queues': [
        Queue(
            ACTION_LIST_EVENT_QUEUE,
            exchange=Exchange('action_list_ex'),
            routing_key='action_list_route',
            durable=True,
        ),
    ],
    'timezone': 'UTC',
    'task_routes': {
        'initial_task': {
            'queue': ACTION_LIST_EVENT_QUEUE
        },
        'subsequent_task': {
            'queue': ACTION_LIST_EVENT_QUEUE
        }

    },
    'beat_schedule': {
        'action-initial-task': {
            'task': 'initial_task',
            'schedule': timedelta(seconds=10),
        },
    },
}

celery_app.conf.update(celery_config)

class BaseTask(Task):
    def foo():
        return ""

@celery_app.task(
    name='initial_task',
    base=BaseTask,
    bind=True,
    acks_late=True
)
def initial_task(self):
    logger.info("creating group")

    worker_group = group([subsequent_task.s()])
    logger.info("group created, applying async")
    worker_group.apply_async()

@celery_app.task(
    name='subsequent_task',
    base=BaseTask,
    bind=True,
    acks_late=True
)
def subsequent_task(self):
    logger.info("executing subsequent task")
