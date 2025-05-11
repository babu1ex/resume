import socket
import threading
import queue as queue_module
import argparse
import json
import re
from collections import Counter
import requests  # pylint: disable=import-error


class Worker(threading.Thread):  # pylint: disable=too-many-instance-attributes

    def __init__(self, task_queue,  # pylint: disable=too-many-arguments
                 top_k, counter,
                 counter_lock,
                 success_counter,
                 error_counter,
                 print_lock):
        super().__init__()
        self.task_queue = task_queue
        self.top_k = top_k
        self.counter = counter
        self.counter_lock = counter_lock
        self.success_counter = success_counter
        self.error_counter = error_counter
        self._print_lock = print_lock
        self.daemon = True

    def run(self):
        while True:
            url = None
            client_socket = None
            try:
                self.name = f"Worker #{threading.get_ident()}"
                url, client_socket = self.task_queue.get()

                if url is None:
                    with self._print_lock:
                        print(f"[{self.name}] Завершение — получен сигнал остановки", flush=True)
                    self.task_queue.task_done()
                    break
                with self._print_lock:
                    print(f"[{self.name}] Получен URL: {url}")

                response = requests.get(url, timeout=5)
                text = response.text
                words = re.findall(r'\w+', text)
                local_counter = Counter(words)
                top = local_counter.most_common(self.top_k)
                json_string = json.dumps(dict(top))
                client_socket.send(json_string.encode())
                client_socket.close()

                with self.counter_lock:
                    self.success_counter[0] += 1
                    self.counter[0] += 1
                    with self._print_lock:
                        print(f"[{self.name}] Успешно обработано: {self.success_counter[0]}")

            except Exception:  # pylint: disable=broad-exception-caught
                with self.counter_lock:
                    self.error_counter[0] += 1
                    self.counter[0] += 1
                    with self._print_lock:
                        print(f"[{self.name}] Ошибка обработки. Ошибок всего: {self.error_counter[0]}")

                if client_socket:
                    try:
                        client_socket.send(b'{"error": "Failed to process URL"}')
                        client_socket.close()
                    except Exception:  # pylint: disable=broad-exception-caught
                        pass

            finally:
                if url is not None:
                    self.task_queue.task_done()


class MasterServer:  # pylint: disable=too-many-instance-attributes, disable=too-few-public-methods

    def __init__(self, num_workers, top_k, lock_for_print):
        self.num_workers = num_workers
        self.top_k = top_k
        self.task_queue = queue_module.Queue()
        self.counter_lock = threading.Lock()
        self.counter = [0]
        self.success_counter = [0]
        self.error_counter = [0]
        self.workers = []
        self._print_lock = lock_for_print

        for i in range(num_workers):
            worker = Worker(
                self.task_queue, self.top_k,
                self.counter, self.counter_lock,
                self.success_counter, self.error_counter,
                self._print_lock
            )
            worker.start()
            self.workers.append(worker)
            with self._print_lock:
                print(f"[MASTER] Запущен воркер #{i+1} (ID потока: {worker.ident})")

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 20000))
        s.listen()
        s.settimeout(1)

        try:
            while True:
                try:
                    client_socket, _ = s.accept()
                    data = client_socket.recv(1024)
                    url = data.decode().strip()
                    self.task_queue.put((url, client_socket))

                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("[MASTER] Остановка сервера (Ctrl+C)")
            for _ in self.workers:
                self.task_queue.put((None, None))
            for worker in self.workers:
                worker.join()

            print("[MASTER] Все воркеры закончили.")
            print(f"[MASTER] Всего успешно обработано: {self.success_counter[0]}")
            print(f"[MASTER] Всего с ошибкой: {self.error_counter[0]}")


def start_server():
    lock_print = threading.Lock()
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", type=int, default=2, help="Количество воркеров")
    parser.add_argument("-k", type=int, default=4, help="Сколько слов выводить")
    args = parser.parse_args()

    master = MasterServer(num_workers=args.w, top_k=args.k, lock_for_print=lock_print)
    master.start()


if __name__ == "__main__":
    start_server()
