CELERY_BROKER_URL = 'redis://192.168.2.50:6379/0'
CELERY_RESULT_BACKEND = 'redis://192.168.2.50:6379/15'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
CELERY_ACCEPT_CONTENT = ['json']
BROKER_CONNECTION_TIMEOUT = 1
