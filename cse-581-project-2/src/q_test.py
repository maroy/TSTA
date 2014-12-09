import os
import time
import Queue
import random
import multiprocessing


def process_print(l,msg):
    with l:
        print "{0}: {1}".format(os.getpid(), msg)


def worker(q,l):
    process_print(l, "worker started.")

    while True:
        try:
            x = q.get(False)
            time.sleep(random.random())
            process_print(l, "got: " + str(x))
        except Queue.Empty:
            process_print(l, "worker done.")
            break


def main():
    q = multiprocessing.Queue()
    l = multiprocessing.Lock()
    for i in range(0,100):
        q.put(i)

    processes = []
    for i in range(0,6):
        p = multiprocessing.Process(target = worker, args = (q,l))
        p.daemon = True
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    process_print(l, "main done.")

if __name__ == "__main__":
    main()
