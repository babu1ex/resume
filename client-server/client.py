import argparse
import socket
import time
from queue import Queue
import threading


def worker(url_queue):  # pylint: disable=redefined-outer-name
    while not url_queue.empty():
        try:
            url = url_queue.get_nowait()  # pylint: disable=redefined-outer-name
            with socket.socket() as sock:
                sock.connect(('127.0.0.1', 20000))
                sock.send(url.encode())
                data = sock.recv(4096)
                print(f"\nОтвет для {url}:\n{data.decode()}", flush=True)

        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"[ERROR] Поток не смог обработать URL {url}. Ошибка: {type(e).__name__}: {e}", flush=True)

        finally:
            url_queue.task_done()


def start_threads(url_queue, num_threads):
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(url_queue,))
        t.start()
        threads.append(t)
    return threads


def main():
    parser = argparse.ArgumentParser(description="Клиент для многопоточной обкачки URL")
    parser.add_argument('threads', type=int, help="Количество потоков клиента")
    parser.add_argument('url_file', help="Файл с URL-ами")
    args = parser.parse_args()

    url_queue = Queue()

    with open(args.url_file, "r", encoding='UTF-8') as f:
        for line in f:
            url = line.strip()
            if url:
                url_queue.put(url)

    start_time = time.time()

    print(f"Количество URL в очереди: {url_queue.qsize()}")

    threads = start_threads(url_queue, args.threads)

    for t in threads:
        t.join()

    print("\nВсе URL обработаны.")
    print(f"Время выполнения {time.time() - start_time:.2f} секунд")


if __name__ == "__main__":
    main()
