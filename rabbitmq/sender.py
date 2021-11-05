import pika
import time
import json

credentials = pika.PlainCredentials('root','password')

connection = pika.BlockingConnection(pika.ConnectionParameters('10.x.x.x',
                                                               1234,
                                                               credentials=credentials
                                                               )
                                     )

channel = connection.channel()

channel.queue_declare(queue='hello')

# content = "this is test message"
content = time.asctime( time.localtime(time.time()) )

# class  Content:
# 	def __init__(self):
# 		self.name = "test_name"

# content = Content()


channel.basic_publish(exchange='',
                      routing_key='hello',
                      # body=json.dumps(content),
                      # properties=pika.BasicProperties(delivery_mode = 2,)
                      body=content
                      )
# channel.start_consuming()
connection.close()