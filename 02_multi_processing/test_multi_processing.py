
import os
import multiprocessing as mp
from multiprocessing import Pool
import threading
import time
import datetime
from typing import Callable
from functools import partial
from torch.utils.data import Dataset


def print_decorator(func: Callable, text: str) -> Callable:
    def printing():
        print(text)
        start = int(time.time())
        func()
        end = int(time.time())
        print(f"Number of Core : {str(mp.cpu_count())}")
        print(f"***run time(sec) : {end-start}")
    return printing

print_nm = partial(print_decorator, text = "non_multiprocess")
print_m = partial(print_decorator, text = "multiprocess")


@print_nm
def non_multiprocess():
    for i in range(1, 12):
        work_func(i)

@print_m
def multiprocess():
    # 멀티 프로세싱을 위한 CPU 숫자 확인 및 풀 만들기
    num_cores = mp.cpu_count()
    pool = Pool(num_cores)

    object_list = [i for i in range(1, 100)]

    # 멀티 프로세싱 워커 호출
    pool.map(work_func, object_list)

    # 메모리 릭 방지 위해 사용
    pool.close()
    pool.join()


def work_func(x):
    print(f"time: {str(datetime.datetime.today())} | value: {str(x)} | PID: {str(os.getpid())}")
    time.sleep(1)


if __name__ == '__main__':
# execute only if run as a script
    non_multiprocess()
    multiprocess()

   