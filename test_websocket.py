from websocket import create_connection
from functools import reduce
import multiprocessing
import threading
import timeit
import sys
import time


class test_class(object):
    def func():
        print("hello world")

list1 = [test_class] * 1000
list2 = [list1] * 100


def test_run_time():
	time1 = timeit.timeit("users = reduce(lambda x,y: x + y, list2);list(map(lambda waiter: waiter.func(), users))","from __main__ import list2;from functools import reduce",number=100)
	time2 = timeit.timeit("[y.func() for x in list2 for y in x ]","from __main__ import list2",number=100)
	print(time1)
	print(time2)


class connect(threading.Thread):

    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id

    def run(self):
        ws = create_connection("ws://127.0.0.1:8888/chatsocket?id="+str(self.id))
        while 1:
            time.sleep(.5)
            ws.send('{"body":"Hello, World","type":"1"}')
            result =  ws.recv()
            print("Received '%s'" % result)


def run_threading(num,id):
    for num in range(num):
        thread = connect(id)
        thread.start()

if __name__ == "__main__":
    #test_run_time()
    run_threading(50,1)
    run_threading(50,2)
#ws.close()
