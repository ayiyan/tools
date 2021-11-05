import pika
import json

credentials = pika.PlainCredentials('root','password')

connection = pika.BlockingConnection(pika.ConnectionParameters('10.x.x.x',
                                                               1234,
                                                               credentials=credentials
                                                               )
                                     )



channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print("-"*11)
    print(ch,method, properties, body)
    channel.basic_ack(method.delivery_tag)
    channel.stop_consuming()
    


while True:
    method_frame, header_frame, body = channel.basic_get('hello')
    if method_frame:
        s2 = bytes.decode(body)
        print(s2)
        # content=body.decode()
        # content=json.loads(content)
        # print(content["name"])
        channel.basic_ack(method_frame.delivery_tag)
    else:
        # print('No message returned')
        break
    
# channel.basic_consume(queue='hello',
#                       on_message_callback=callback,
#                       )



# channel.start_consuming()

# channel.Sel
# xx = channel.consume(queue='hello')
# print(xx.__next__())

# for method, properties, body in channel.consume('hello'):
#     if body is not None:
#         print(body)
#         channel.basic_ack(method.delivery_tag)
#     else:
#         break
    
# while True:
#     method, properties, body =  channel.consume('hello')
#     print("-")
#     if body is not None:
#         print(body)
#         channel.basic_ack(method.delivery_tag)
#     else:
#         break