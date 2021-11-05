from __future__ import  absolute_import
from proj.celery import app
import time

@app.task
def add():
	time.sleep(30)
	return("123")

@app.task
def add2():
	time.sleep(60)
	return("456")
