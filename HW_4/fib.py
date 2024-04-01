import time
from threading import Thread
import multiprocessing


def fib(n):
    """Функция подсчета чисел Фибоначчи"""
    a = 0
    b = 1
    for _ in range(n):
        a, b = b, a + b
    return a


def run_sync(num_runs, n):
    for _ in range(num_runs):
        fib(n)


def run_threads(num_threads, n):
    threads = []
    for _ in range(num_threads):
        t = Thread(target=fib, args=(n,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


def run_processes(num_processes, n):
    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(target=fib, args=(n,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()


if __name__ == "__main__":
    n = 500000  # номер числа Фибоначчи
    num_runs = 10  # количество синхронных запусков
    num_threads = 10  # количество потоков
    num_processes = 10  # количество процессов

    with open("artifacts/hw1_results.txt", "w") as file:
        file.write("Method\t\tTime\n")

        start_time = time.time()
        run_sync(num_runs, n)
        file.write("Sync\t\t{:.4f}\n".format(time.time() - start_time))

        start_time = time.time()
        run_threads(num_threads, n)
        file.write("Threads\t\t{:.4f}\n".format(time.time() - start_time))

        start_time = time.time()
        run_processes(num_processes, n)
        file.write("Processes\t{:.4f}".format(time.time() - start_time))
