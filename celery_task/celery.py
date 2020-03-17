from celery import Celery

# 标注celery的名称  以及task的路径
celery_app = Celery('WeRobot', include=['celery_task.tasks'])

celery_app.config_from_object('celery_task.celeryconfig')

celery_app.conf.update(
    result_expires=60 * 60 * 24
)
