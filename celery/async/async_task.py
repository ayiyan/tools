import sys
import time 

from celery import Celery
 
celery = Celery('tasks',
	backend='redis://192.168.2.50:6379/15',
	broker='redis://192.168.2.50:6379/0'
	)

from celery.utils.log import get_task_logger 
logger = get_task_logger(__name__)
 

#@celery.task 
def execute_job(self):
	print("111111")	
	time.sleep(3600)
	# logger.info('===================> exec_task_order_overtime order_id=%s' % order_id)
