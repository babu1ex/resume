import json
import sys
import threading
from queue import Queue
from unittest.mock import patch, MagicMock
from server import Worker, MasterServer, start_server


def test_worker_initialization():
    queue = Queue()
    worker = Worker(
        task_queue=queue,
        top_k=5,
        counter=[0],
        counter_lock=threading.Lock(),
        success_counter=[0],
        error_counter=[0],
        print_lock=threading.Lock()
    )
    assert isinstance(worker, threading.Thread)
    assert worker.daemon is True


def test_worker_successful_processing():
    queue = Queue()
    url = "http://example.com"
    mock_socket = MagicMock()

    queue.put((url, mock_socket))
    queue.put((None, None))

    with patch("server.requests.get") as mock_get:
        mock_get.return_value.text = "hello world hello world hello"
        worker = Worker(
            task_queue=queue,
            top_k=1,
            counter=[0],
            counter_lock=threading.Lock(),
            success_counter=[0],
            error_counter=[0],
            print_lock=threading.Lock()
        )
        worker.start()
        worker.join()

    mock_socket.send.assert_called()
    sent = mock_socket.send.call_args[0][0]
    data = json.loads(sent.decode())
    assert isinstance(data, dict)
    assert len(data) == 1
    assert "hello" in data


def test_worker_fail():
    queue = Queue()
    url = "http://badurl.com"
    mock_socket = MagicMock()

    queue.put((url, mock_socket))
    queue.put((None, None))

    with patch("server.requests.get", side_effect=Exception("fail")):
        worker = Worker(
            task_queue=queue,
            top_k=3,
            counter=[0],
            counter_lock=threading.Lock(),
            success_counter=[0],
            error_counter=[0],
            print_lock=threading.Lock()
        )
        worker.start()
        worker.join()

    mock_socket.send.assert_called()
    sent = mock_socket.send.call_args[0][0]
    data = json.loads(sent.decode())
    assert "error" in data


def test_worker_handles_send_exception():
    queue = Queue()
    url = "http://example.com"
    mock_socket = MagicMock()
    mock_socket.send.side_effect = Exception("send failed")

    queue.put((url, mock_socket))
    queue.put((None, None))

    with patch("server.requests.get", side_effect=Exception("request failed")):
        worker = Worker(
            task_queue=queue,
            top_k=2,
            counter=[0],
            counter_lock=threading.Lock(),
            success_counter=[0],
            error_counter=[0],
            print_lock=threading.Lock()
        )
        worker.start()
        worker.join()

    assert worker.error_counter[0] == 1


def test_worker_stops_on_none_signal():
    queue = Queue()
    queue.put((None, None))

    worker = Worker(
        task_queue=queue,
        top_k=1,
        counter=[0],
        counter_lock=threading.Lock(),
        success_counter=[0],
        error_counter=[0],
        print_lock=threading.Lock()
    )
    worker.start()
    worker.join()
    assert not worker.is_alive()


def test_masterserver_creates_workers():
    lock = threading.Lock()
    master = MasterServer(num_workers=3, top_k=5, lock_for_print=lock)
    assert len(master.workers) == 3
    for w in master.workers:
        assert isinstance(w, Worker)


def test_masterserver_enqueue_and_process_one_task():
    lock = threading.Lock()
    master = MasterServer(num_workers=1, top_k=2, lock_for_print=lock)
    mock_socket = MagicMock()
    url = "http://example.com"

    with patch("server.requests.get") as mock_get:
        mock_get.return_value.text = "a a b b c"
        master.task_queue.put((url, mock_socket))
        master.task_queue.put((None, None))
        master.task_queue.join()

    mock_socket.send.assert_called()
    sent = mock_socket.send.call_args[0][0]
    data = json.loads(sent.decode())
    assert isinstance(data, dict)
    assert len(data) == 2
    assert master.success_counter[0] == 1


def test_masterserver_processes_multiple_tasks():
    lock = threading.Lock()
    master = MasterServer(num_workers=2, top_k=3, lock_for_print=lock)
    sock1, sock2 = MagicMock(), MagicMock()
    master.task_queue.put(("http://one", sock1))
    master.task_queue.put(("http://two", sock2))
    master.task_queue.put((None, None))
    master.task_queue.put((None, None))

    with patch("server.requests.get") as mock_get:
        mock_get.return_value.text = "x x y y z"
        master.task_queue.join()

    assert sock1.send.called and sock2.send.called
    assert master.success_counter[0] == 2


def test_masterserver_worker_shutdown():
    lock = threading.Lock()
    master = MasterServer(num_workers=2, top_k=1, lock_for_print=lock)
    master.task_queue.put((None, None))
    master.task_queue.put((None, None))
    master.task_queue.join()

    for w in master.workers:
        w.join()
        assert not w.is_alive()


def test_masterserver_keyboard_interrupt(monkeypatch):
    lock = threading.Lock()
    master = MasterServer(num_workers=1, top_k=1, lock_for_print=lock)
    fake_socket = MagicMock()
    fake_socket.accept.side_effect = KeyboardInterrupt
    monkeypatch.setattr("server.socket.socket", lambda *args, **kwargs: fake_socket)

    master.start()
    for w in master.workers:
        assert not w.is_alive()


def test_start_server_runs_master(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["server.py", "-w", "1", "-k", "2"])
    # pylint: disable=too-few-public-methods, unused-variable

    class DummyMaster:
        def __init__(self, *args, **kwargs):
            pass

        def start(self):
            print("Server started")

    monkeypatch.setattr("server.MasterServer", DummyMaster)
    start_server()
    captured = capsys.readouterr()
    assert "Server started" in captured.out
