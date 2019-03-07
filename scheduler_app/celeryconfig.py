from celery.schedules import crontab


CELERY_IMPORTS = ('scheduler_app.tasks')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'Asia/Singapore'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    # Check every minute for scheduled emails to be sent at that time
    'check_scheduled_emails': {
        'task': 'scheduler_app.tasks.check_scheduled_emails',
        'schedule': crontab(minute="*"),
    }
}
