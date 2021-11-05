import pickle
import multiprocessing
import time

import redis


def TargetObject():
    for i in range(0, 1200):
        time.sleep(1)


if __name__ == "main":
    print("-" * 11)
    r = redis.Redis(host='192.168.2.50', port=6379, db=1)
    process_obj = multiprocessing.Process(target=TargetObject)
    process_obj.start()
    print(process_obj.is_alive)
    pickled_object = pickle.dumps(process_obj)
    r.set('some_key', pickled_object)
    unpacked_object = pickle.loads(r.get('some_key'))
    print(unpacked_object.__dict__)
