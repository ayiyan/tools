from celery import Celery
from celery.result import AsyncResult

celery = Celery('tasks',
	backend='redis://127.0.0.1:6379/15',
	broker='redis://127.0.0.1:6379/0'
	)

push_task_id = celery.send_task('proj.tasks.add')

job_id = str(push_task_id.id)
print(job_id)

push_task_id = celery.send_task('proj.tasks.add2')
job_id = str(push_task_id.id)
print(job_id)

#task = celery.AsyncResult(job_id)
#print(task.status)
#print(task.result)