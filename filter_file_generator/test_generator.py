import unittest
from unittest import mock

from generator import filter_file


class TestFilterFile(unittest.TestCase):

    file = 'Я не завидую орлам\nЛетящим в НЕБЕ в высоко\nЯ сам бываю часто там\nГде видно на 100 верст кругом'
    mock_open = mock.mock_open(read_data=file)

    @mock.patch("builtins.open", mock_open)
    def test_file_upper_registr(self):

        filtr_words_lst = ['небе', 'видно']
        stop_words_lst = ['видно']
        expected_lines = 'Летящим в НЕБЕ в высоко'
        result = filter_file("stihi", filtr_words_lst, stop_words_lst)

        self.assertEqual(next(result), expected_lines)

        with self.assertRaises(StopIteration):
            next(result)

    file = 'Я не завидую орлам\nЛетящим в небе в высоко\nЯ сам бываю часто там\nГде видно на 100 верст кругом'
    mock_open = mock.mock_open(read_data=file)

    @mock.patch("builtins.open", mock_open)
    def test_fwords_upper_registr(self):

        filtr_words_lst = ['НЕБЕ', 'видно']
        stop_words_lst = ['видно']
        expected_lines = 'Летящим в небе в высоко'
        result = filter_file("stihi", filtr_words_lst, stop_words_lst)

        self.assertEqual(next(result), expected_lines)

        with self.assertRaises(StopIteration):
            next(result)

    file = 'Я не завидую орлам\nЛетящим в небе в высоко\nЯ сам бываю часто там\nГде видно на 100 верст кругом'
    mock_open = mock.mock_open(read_data=file)

    @mock.patch("builtins.open", mock_open)
    def test_swords_upper_registr(self):
        filtr_words_lst = ['небе', 'высоко']
        stop_words_lst = ['ВЫСОКО']
        result = filter_file("stihi", filtr_words_lst, stop_words_lst)

        with self.assertRaises(StopIteration):
            next(result)

    file = 'Я не завидую орлам\nЛетящим в небе в высоко\nЯ сам бываю часто там\nГде видно на 100 верст кругом'
    mock_open = mock.mock_open(read_data=file)

    @mock.patch("builtins.open", mock_open)
    def test_fwords_works(self):
        filtr_words_lst = ['орлам', 'высоко']
        stop_words_lst = ['высоко']
        expected_lines = 'Я не завидую орлам'
        result = filter_file("stihi", filtr_words_lst, stop_words_lst)

        self.assertEqual(next(result), expected_lines)

        with self.assertRaises(StopIteration):
            next(result)

    file = 'Я не завидую орлам\nЛетящим в небе в высоко\nЯ сам бываю часто там\nГде видно на 100 верст кругом'
    mock_open = mock.mock_open(read_data=file)

    @mock.patch("builtins.open", mock_open)
    def test_swords_works(self):
        filtr_words_lst = ['небе', 'высоко']
        stop_words_lst = ['высоко']
        result = filter_file("MyFstihiile", filtr_words_lst, stop_words_lst)

        with self.assertRaises(StopIteration):
            next(result)

    file = 'Я не завидую орлам\nЛетящим в небе в высоко\nЯ сам бываю часто там\nГде видно на 100 верст кругом'
    mock_open = mock.mock_open(read_data=file)

    @mock.patch("builtins.open", mock_open)
    def test_empty_lists(self):
        filtr_words_lst = []
        stop_words_lst = []
        result = filter_file("stihi", filtr_words_lst, stop_words_lst)

        with self.assertRaises(StopIteration):
            next(result)

    file = 'Я не завидую орлам\nЛетящим в небе в высоко\nЯ сам бываю часто там\nГде видно на 100 верст кругом'
    mock_open = mock.mock_open(read_data=file)

    @mock.patch("builtins.open", mock_open)
    def test_s_empty_list(self):
        filtr_words_lst = ['небе', 'высоко']
        stop_words_lst = []
        expected_lines = 'Летящим в небе в высоко'
        result = filter_file("stihi", filtr_words_lst, stop_words_lst)

        self.assertEqual(next(result), expected_lines)
        with self.assertRaises(StopIteration):
            next(result)

    file = 'Я не завидую орлам\nЛетящим в небе в высоко\nЯ сам бываю часто там\nГде видно на 100 верст кругом'
    mock_open = mock.mock_open(read_data=file)

    @mock.patch("builtins.open", mock_open)
    def test_f_empty_list(self):
        filtr_words_lst = []
        stop_words_lst = ['высоко']
        result = filter_file("stihi", filtr_words_lst, stop_words_lst)

        with self.assertRaises(StopIteration):
            next(result)

    file = 'Я не завидую орлам\nЛетящим в НЕБЕ в высоко\nЯ сам бываю часто там\nГде видно на 100 верст кругом'
    mock_open = mock.mock_open(read_data=file)

    @mock.patch("builtins.open", mock_open)
    def test_f_repeat(self):
        filtr_words_lst = ['небе', 'небе']
        stop_words_lst = ['видно']
        expected_lines = 'Летящим в НЕБЕ в высоко'
        result = filter_file("stihi", filtr_words_lst, stop_words_lst)

        self.assertEqual(next(result), expected_lines)

        with self.assertRaises(StopIteration):
            next(result)

    file = 'Я не завидую орлам\nЛетящим в НЕБЕ в высоко\nЯ сам бываю часто там\nГде видно на 100 верст кругом'
    mock_open = mock.mock_open(read_data=file)

    @mock.patch("builtins.open", mock_open)
    def test_s_repeat(self):
        filtr_words_lst = ['небе']
        stop_words_lst = ['высоко', 'высоко']
        result = filter_file("stihi", filtr_words_lst, stop_words_lst)

        with self.assertRaises(StopIteration):
            next(result)

    file = 'Я не завидую орлам\nЛетящим в НЕБЕ в высоко\nЯ сам бываю часто там\nГде видно на 100 верст кругом'
    mock_open = mock.mock_open(read_data=file)

    @mock.patch("builtins.open", mock_open)
    def test_f_not_full(self):
        filtr_words_lst = ['неб']
        stop_words_lst = ['бываю']
        result = filter_file("stihi", filtr_words_lst, stop_words_lst)

        with self.assertRaises(StopIteration):
            next(result)

    file = 'Я не завидую орлам\nЛетящим в НЕБЕ в высоко\nЯ сам бываю часто там\nГде видно на 100 верст кругом'
    mock_open = mock.mock_open(read_data=file)

    @mock.patch("builtins.open", mock_open)
    def test_s_not_full(self):
        filtr_words_lst = ['небе']
        stop_words_lst = ['высо']
        result = filter_file("stihi", filtr_words_lst, stop_words_lst)
        expected_lines = 'Летящим в НЕБЕ в высоко'

        self.assertEqual(next(result), expected_lines)

        with self.assertRaises(StopIteration):
            next(result)

    file = 'Я не завидую орлам\nЛетящим в НЕБЕ в высоко\nЯ сам бываю часто там\nГде видно на 100 верст кругом'
    mock_open = mock.mock_open(read_data=file)

    @mock.patch("builtins.open", mock_open)
    def test_file_equals(self):
        filtr_words_lst = ['небе']
        stop_words_lst = ['небе']
        result = filter_file("stihi", filtr_words_lst, stop_words_lst)

        with self.assertRaises(StopIteration):
            next(result)

    file = ''
    mock_open = mock.mock_open(read_data=file)

    @mock.patch("builtins.open", mock_open)
    def test_file_empty(self):
        filtr_words_lst = ['небе']
        stop_words_lst = ['бываю']
        result = filter_file("stihi", filtr_words_lst, stop_words_lst)

        with self.assertRaises(StopIteration):
            next(result)

    file = 'Я не завидую орлам\nНЕБЕ\nЯ сам бываю часто там\nГде видно на 100 верст кругом'
    mock_open = mock.mock_open(read_data=file)

    @mock.patch("builtins.open", mock_open)
    def test_stop_match_string(self):
        filtr_words_lst = ['небе']
        stop_words_lst = ['НЕБЕ']
        result = filter_file("stihi", filtr_words_lst, stop_words_lst)

        with self.assertRaises(StopIteration):
            next(result)

    file = 'Я не завидую орлам\nЛетящим в НЕБЕ в высоко\nЯ сам бываю часто там\nГде видно на 100 верст кругом'
    mock_open = mock.mock_open(read_data=file)

    @mock.patch("builtins.open", mock_open)
    def test_filtr_one_symbol(self):
        filtr_words_lst = ['я']
        stop_words_lst = ['небе']
        result = filter_file("stihi", filtr_words_lst, stop_words_lst)
        expected_lines1 = 'Я не завидую орлам'
        expected_lines2 = 'Я сам бываю часто там'

        self.assertEqual(next(result), expected_lines1)
        self.assertEqual(next(result), expected_lines2)

        with self.assertRaises(StopIteration):
            next(result)

    file = 'Я не завидую орлам\nЛетящим в НЕБЕ в высоко\nЯ сам бываю часто там\nГде видно на 100 верст кругом'
    mock_open = mock.mock_open(read_data=file)

    @mock.patch("builtins.open", mock_open)
    def test_stop_one_symbol(self):
        filtr_words_lst = ['где']
        stop_words_lst = ['е']
        result = filter_file("stihi", filtr_words_lst, stop_words_lst)
        expected_lines1 = 'Где видно на 100 верст кругом'

        self.assertEqual(next(result), expected_lines1)

        with self.assertRaises(StopIteration):
            next(result)

    file = 'орлам\nЛетящим в НЕБЕ в высоко\nЯ сам бываю часто там\nГде видно на 100 верст кругом'
    mock_open = mock.mock_open(read_data=file)

    @mock.patch("builtins.open", mock_open)
    def test_filtr_match_string(self):
        filtr_words_lst = ['орлам']
        stop_words_lst = ['небе']
        result = filter_file("stihi", filtr_words_lst, stop_words_lst)
        expected_lines1 = 'орлам'

        self.assertEqual(next(result), expected_lines1)

        with self.assertRaises(StopIteration):
            next(result)
