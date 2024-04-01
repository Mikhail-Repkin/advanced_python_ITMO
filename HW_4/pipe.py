from multiprocessing import Queue, Pipe, Process
import time
from codecs import encode


def pr_a(queue_main_a, queue_a_b):
    while True:
        message = queue_main_a.get()
        print(f"{time.strftime('%H:%M:%S')} в процесс A: {message}")
        message_lower = message.lower()
        queue_a_b.put(message_lower)
        time.sleep(5)


def pr_b(queue_a_b, queue_b_main):
    while True:
        message = queue_a_b.get()
        print(f"{time.strftime('%H:%M:%S')} в процесс B: {message}")
        encoded_message = encode(message, "rot_13")
        queue_b_main.put(encoded_message)


if __name__ == "__main__":
    queue_main_a = Queue()
    queue_a_b = Queue()
    queue_b_main = Queue()

    pipe_ab = Pipe()

    process_a = Process(target=pr_a, args=(queue_main_a, queue_a_b))
    process_b = Process(target=pr_b, args=(queue_a_b, queue_b_main))

    process_a.start()
    process_b.start()

    try:
        while True:
            message = input("Enter a message or 'QUIT' to exit:")
            if message == 'QUIT':
                break
            print(f"{time.strftime('%H:%M:%S')} input: {message}")
            queue_main_a.put(message.strip())
            message = queue_b_main.get()
            print(f"{time.strftime('%H:%M:%S')} output: {message}")
    finally:
        process_a.terminate()
        process_b.terminate()
