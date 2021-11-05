from celery import Celery
from celery.result import AsyncResult

celery = Celery('tasks',
	backend='redis://10.x.x.x:6379/15',
	broker='redis://10.x.x.x:6379/0'
	)


# task = celery.AsyncResult("1bb1325b-9361-450f-adbb-9cea8185ebbb")
# print(task.status)
# print(task.result)

# xx = celery.AsyncResult("1bb1325b-9361-450f-adbb-9cea8185ebbb").revoke()
# print(xx)

task = celery.control.revoke("b4e036f9-de70-466b-9eed-594f889c6dd7")
print(task)
# print(task.result)


task = celery.AsyncResult("b4e036f9-de70-466b-9eed-594f889c6dd7")
print(task.status)
print(task.result)