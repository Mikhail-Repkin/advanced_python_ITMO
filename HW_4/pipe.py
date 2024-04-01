from multiprocessing import Queue, Pipe, Process
import time
from codecs import encode
from queue import Empty


def pr_a(queue_main_a, queue_a_b):
    while True:
        try:
            message = queue_main_a.get(block=False)
            message_lower = message.lower()
            queue_a_b.put(message_lower, block=False)
            time.sleep(5)
        except Empty:
            pass


def pr_b(queue_a_b, queue_b_main):
    while True:
        try:
            message = queue_a_b.get(block=False)
            encoded_message = encode(message, "rot_13")
            queue_b_main.put({f"{message}": encoded_message}, block=False)
        except Empty:
            pass


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
            message = input(f"{time.strftime('%H:%M:%S')} " +
                            "Enter a message or 'QUIT' to exit:")
            if message == 'QUIT':
                break
            print(f"{time.strftime('%H:%M:%S')} input: {message}")
            queue_main_a.put(message.strip(), block=False)
            try:
                message = queue_b_main.get(block=False)
                print(f"{time.strftime('%H:%M:%S')} output для: {message}")
            except Empty:
                pass
    finally:
        process_a.terminate()
        process_b.terminate()
