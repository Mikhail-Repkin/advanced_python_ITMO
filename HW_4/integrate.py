import math
from concurrent.futures import (ThreadPoolExecutor,
                                ProcessPoolExecutor,
                                as_completed)
import time
import logging
from multiprocessing import cpu_count


logging.basicConfig(filename='artifacts/integration_log.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def integrate_worker(f, a, start, end, step):
    acc = 0
    for i in range(start, end):
        acc += f(a + i * step) * step
    return acc


def integrate(f, a, b, pool_executor, n_jobs=1, n_iter=10000000):
    """
    Функция выполняет численное интегрирование функции f \n
    на заданном интервале [a, b] с использованием метода прямоугольников.

    Аргументы:
        f (callable): Функция, которую необходимо интегрировать.
        a (float): Нижний предел интегрирования.
        b (float): Верхний предел интегрирования.
        executors (class): Пул потоков.
        n_jobs (int, optional): Количество потоков/процессов.
        n_iter (int, optional): Количество итераций интегрирования.

    Возвращает:
        float: Приближенное значение интеграла на интервале [a, b].
    """
    step = (b - a) / n_iter  # шаг интегрирования
    chunk_size = n_iter // n_jobs  # количество итераций на одну джобу
    remainder = n_iter % n_jobs  # остаток итераций

    with pool_executor(max_workers=n_jobs) as executor:
        futures = []
        start = 0
        for i in range(n_jobs):
            end = start + chunk_size + (remainder if i == (n_jobs-1) else 0)
            logging.info(f"Старт воркера {i+1}/{n_jobs} " +
                         f"для диапазона итераций {start}-{end}")
            futures.append(executor.submit(integrate_worker,
                                           f, a, start, end, step))
            start = end

        total = sum(future.result()
                    for future in as_completed(futures))
        logging.info("Завершение работы всех воркеров\n")

    return total


def compare_execution_times(f, a, b, n_jobs_list, n_iter=10000000):
    """Cравнивает время выполнения функции интегрирования \n
    при разном числе n_jobs и при использовании ThreadPoolExecutor \n
    и ProcessPoolExecutor.

    Аргументы:
    f (callable): Функция, которую необходимо проинтегрировать.
    a (float): Нижний предел интегрирования.
    b (float): Верхний предел интегрирования.
    n_jobs_list (list): Список с разными значениями n_jobs.
    n_iter (int, optional): Количество итераций для интегрирования.
    """
    with open("artifacts/execution_times_comparison.txt", "w") as file:
        for executor_type in [ThreadPoolExecutor, ProcessPoolExecutor]:
            for n_jobs in n_jobs_list:
                logging.info(f"Старт {executor_type.__name__}, " +
                             f"количество jobs: {n_jobs}")
                start_time = time.time()
                integrate(f, a, b,
                          executor_type,
                          n_jobs=n_jobs,
                          n_iter=n_iter)

                file.write(str(f"{executor_type.__name__}, jobs: {n_jobs}, " +
                               "время выполнения: " +
                               f"{time.time() - start_time:.4f}s\n"))


if __name__ == "__main__":
    n_jobs_list = list(range(1, cpu_count() * 2 + 1))
    f = math.cos
    a = 0
    b = math.pi / 2

    compare_execution_times(f, a, b, n_jobs_list)
