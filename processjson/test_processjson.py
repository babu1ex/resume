import unittest
from unittest import mock

from processjson import process_json


class TestProcessJson(unittest.TestCase):

    def test_all_keys(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ['key1', 'key2']
        tokens = ["WORD1", "word2"]

        callback_mock = mock.Mock()
        process_json(json_str, required_keys, tokens, callback_mock)

        expected_calls = [
            mock.call("key1", "WORD1"),
            mock.call("key1", "word2"),
            mock.call("key2", "word2")]

        self.assertEqual(callback_mock.mock_calls, expected_calls)

    def test_empty_keys(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = []
        tokens = ["WORD1", "word2"]

        callback_mock = mock.Mock()
        process_json(json_str, required_keys, tokens, callback_mock)

        callback_mock.assert_not_called()

    def test_empty_tokens(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ['key1', 'key2']
        tokens = []

        callback_mock = mock.Mock()
        process_json(json_str, required_keys, tokens, callback_mock)

        callback_mock.assert_not_called()

    def test_empty_all(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = []
        tokens = []

        callback_mock = mock.Mock()
        process_json(json_str, required_keys, tokens, callback_mock)

        callback_mock.assert_not_called()

    def test_none_tokens(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ['key1', 'key2']
        tokens = None

        callback_mock = mock.Mock()
        process_json(json_str, required_keys, tokens, callback_mock)

        callback_mock.assert_not_called()

    def test_none_keys(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = None
        tokens = ["WORD1", "word2"]

        callback_mock = mock.Mock()
        process_json(json_str, required_keys, tokens, callback_mock)

        callback_mock.assert_not_called()

    def test_multiple_matches(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3 Word1", "key3": "word3"}'
        required_keys = ['key1', 'key2', 'key3']
        tokens = ["WORD1", "word2", "word3"]

        callback_mock = mock.Mock()
        process_json(json_str, required_keys, tokens, callback_mock)

        expected_calls = [
            mock.call("key1", "WORD1"),
            mock.call("key1", "word2"),
            mock.call("key2", "word2"),
            mock.call("key2", "WORD1"),
            mock.call("key2", "word3"),
            mock.call("key3", "word3"),
        ]
        self.assertCountEqual(callback_mock.mock_calls, expected_calls)

    def test_no_token_match(self):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ['key1', 'key2']
        tokens = ["bebebebababa"]

        callback_mock = mock.Mock()
        process_json(json_str, required_keys, tokens, callback_mock)

        self.assertEqual(callback_mock.mock_calls, [])
