import sys
import threading
from queue import Queue
from unittest.mock import patch, MagicMock

import pytest

from client import worker, start_threads, main


def test_worker_sends_url_and_receives_data():
    url_queue = Queue()
    test_url = "http://example.com"
    url_queue.put(test_url)

    with patch("socket.socket") as mock_socket_class:
        mock_socket = MagicMock()
        mock_socket.recv.return_value = b"response from server"
        mock_socket_class.return_value.__enter__.return_value = mock_socket

        worker(url_queue)

        mock_socket.connect.assert_called_once_with(("127.0.0.1", 20000))
        mock_socket.send.assert_called_once_with(test_url.encode())
        mock_socket.recv.assert_called_once()


def test_worker_with_empty_queue():
    url_queue = Queue()

    with patch("socket.socket") as mock_socket_class:
        mock_socket = MagicMock()
        mock_socket_class.return_value.__enter__.return_value = mock_socket

        worker(url_queue)

        mock_socket.connect.assert_not_called()
        mock_socket.send.assert_not_called()
        mock_socket.recv.assert_not_called()


def test_start_threads_creates_correct_number_of_threads():
    url_queue = Queue()
    url_queue.put("http://example.com")
    num_threads = 5

    threads = start_threads(url_queue, num_threads)

    assert len(threads) == num_threads
    for t in threads:
        assert isinstance(t, threading.Thread)


def test_main_parses_arguments_correctly(tmp_path):
    url_file = tmp_path / "urls.txt"
    url_file.write_text("http://example.com\n")

    test_args = ["client.py", "2", str(url_file)]
    with patch.object(sys, "argv", test_args):
        try:
            main()
        except SystemExit:
            pytest.fail("ошибки при корректных аргументах")


def test_start_threads_and_join_works_correctly():
    url_queue = Queue()
    url_queue.put("http://example.com")
    url_queue.put("http://example.org")

    num_threads = 2
    threads = start_threads(url_queue, num_threads)

    assert len(threads) == num_threads

    for t in threads:
        t.join()
        assert not t.is_alive()


def test_worker_calls_task_done_even_on_exception():
    url_queue = Queue()
    url_queue.put("http://example.com")

    with patch("socket.socket") as mock_socket_class:
        mock_socket = MagicMock()
        mock_socket.connect.side_effect = Exception("Connection failed")
        mock_socket_class.return_value.__enter__.return_value = mock_socket

        worker(url_queue)

    assert url_queue.empty()
