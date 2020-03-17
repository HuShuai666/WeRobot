# coding=utf-8
from celery.schedules import crontab
from kombu import Queue

result_backend = 'redis://localhost:6379/2'
broker_url = 'redis://localhost:6379/3'
timezone = 'Asia/Shanghai'
accept_content = ['json']
task_default_exchange_type = 'direct'
task_serializer = 'json'

task_queues = (
    Queue('queue', routing_key='celery'),
    Queue('queue2', routing_key='celery2'),
    Queue('queue3', routing_key='celery3'),
)
# celery异步任务
task_routes = {
    'celery_upload_media': {
        'queue': 'queue',
        'routing_key': 'celery',
    }
}


# celery的定时任务
# beat_schedule = {
#     'add-every-day': {
#         'task': 'request_weixin',
#         'schedule': crontab(minute='*'),
#         'args':('images',)
#     },
#
# }