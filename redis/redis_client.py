import pickle

import redis

redis_list = []

class ExampleObject:
    def __init__(self):
        self.text = "redis"

test_obj = ExampleObject()

r = redis.Redis(host='192.168.2.50', port=6379, db=0)

pickled_object = pickle.dumps(test_obj)

r.set('some_key', pickled_object)


unpacked_object = pickle.loads(r.get('some_key'))
print(unpacked_object.__dict__)

