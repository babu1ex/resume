
import unittest
from unittest import mock

from deco import parametr_deco


class TestDecorator(unittest.TestCase):

    def test_with_pos_args(self):
        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):
            mock_func = mock.Mock(return_value=3)
            mock_func.__name__ = "mock_func"
            deco_func = parametr_deco(2)(mock_func)

            result = deco_func(1, 2)

            mock_print.assert_has_calls([
                mock.call('run mock_func with positional args = (1, 2), '
                          'keyword kwargs = {}, attempt = 1, result = 3'),
            ], any_order=False)

            self.assertEqual(result, 3)
            self.assertEqual(mock_func.call_count, 1)  # проверяем кол-во перезапусков

    def test_with_keyword_args(self):
        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):
            mock_func = mock.Mock(return_value=3)
            mock_func.__name__ = "mock_func"
            deco_func = parametr_deco(2)(mock_func)

            result = deco_func(x=1, y=2)

            mock_print.assert_has_calls([
                mock.call("run mock_func with positional args = (), "
                          "keyword kwargs = {'x': 1, 'y': 2}, attempt = 1, "
                          "result = 3"),
            ], any_order=False)

            self.assertEqual(result, 3)
            self.assertEqual(mock_func.call_count, 1)  # проверяем кол-во перезапусков

    def test_with_all_types(self):
        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):
            mock_func = mock.Mock(return_value=3)
            mock_func.__name__ = "mock_func"
            deco_func = parametr_deco(2)(mock_func)

            result = deco_func(1, y=2)

            mock_print.assert_has_calls([
                mock.call("run mock_func with positional args = (1,), "
                          "keyword kwargs = {'y': 2}, attempt = 1, "
                          "result = 3"),
            ], any_order=False)

            self.assertEqual(result, 3)
            self.assertEqual(mock_func.call_count, 1)  # проверяем кол-во перезапусков

    def test_zero_attempts(self):
        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):
            mock_func = mock.Mock(return_value=3)
            mock_func.__name__ = "mock_func"
            deco_func = parametr_deco(0)(mock_func)

            result = deco_func(1, y=2)

            mock_print.assert_not_called()

            self.assertEqual(result, None)
            self.assertEqual(mock_func.call_count, 0)  # проверяем кол-во перезапусков

    def test_with_no_arguments(self):
        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):
            mock_func = mock.Mock(return_value=None)
            mock_func.__name__ = "mock_func"
            deco_func = parametr_deco(2)(mock_func)

            result = deco_func()

            mock_print.assert_has_calls([
                mock.call('run mock_func with positional args = (), '
                          'keyword kwargs = {}, attempt = 1, result = None'),
            ], any_order=False)

            self.assertEqual(result, None)
            self.assertEqual(mock_func.call_count, 1)  # проверяем кол-во перезапусков

    def test_with_diff_arguments_types(self):
        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):
            mock_func = mock.Mock(return_value='12')
            mock_func.__name__ = "mock_func"
            deco_func = parametr_deco(2)(mock_func)

            result = deco_func('1', y='2')

            mock_print.assert_has_calls([
                mock.call("run mock_func with positional args = ('1',), "
                          "keyword kwargs = {'y': '2'}, attempt = 1, "
                          "result = 12"),
            ], any_order=False)

            self.assertEqual(result, '12')
            self.assertEqual(mock_func.call_count, 1)  # проверяем кол-во перезапусков

    def test_error(self):
        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):
            mock_func = mock.Mock(side_effect=ValueError())
            mock_func.__name__ = "mock_func"
            deco_func = parametr_deco(2, (ValueError,))(mock_func)

            with self.assertRaises(ValueError):
                deco_func('1', y='2')

            mock_print.assert_has_calls([
                mock.call("run mock_func with positional args = ('1',), "
                          "keyword kwargs = {'y': '2'}, attempt = 1, "
                          "exception = ValueError # нет перезапуска"),
            ], any_order=False)

            self.assertEqual(mock_func.call_count, 1)  # проверяем кол-во перезапусков

    def test_success(self):
        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):
            mock_func = mock.Mock(return_value=12)
            mock_func.__name__ = "mock_func"
            deco_func = parametr_deco(2)(mock_func)

            result = deco_func('1', y='2')

            mock_print.assert_has_calls([
                mock.call("run mock_func with positional args = ('1',), "
                          "keyword kwargs = {'y': '2'}, attempt = 1, "
                          "result = 12"),
            ], any_order=False)

            self.assertEqual(result, 12)
            self.assertEqual(mock_func.call_count, 1)

    def test_error_expected(self):
        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):
            mock_func = mock.Mock(side_effect=ValueError("expected"))
            mock_func.__name__ = "mock_func"
            deco_func = parametr_deco(2, (ValueError,))(mock_func)

            with self.assertRaises(ValueError) as error_type:
                deco_func('1', y='2')

            mock_print.assert_has_calls([
                mock.call("run mock_func with positional args = ('1',), "
                          "keyword kwargs = {'y': '2'}, attempt = 1, "
                          "exception = ValueError # нет перезапуска"),
            ], any_order=False)

            self.assertEqual(mock_func.call_count, 1)
            self.assertEqual(str(error_type.exception), "expected")

    def test_error_unexpected_reraised(self):
        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):
            mock_func = mock.Mock(side_effect=TypeError("unexpected"))
            mock_func.__name__ = "mock_func"
            deco_func = parametr_deco(2)(mock_func)

            with self.assertRaises(TypeError) as error_type:
                deco_func('1', y='2')

            mock_print.assert_has_calls([
                mock.call("run mock_func with positional args = ('1',), "
                          "keyword kwargs = {'y': '2'}, attempt = 1, "
                          "exception = TypeError"),
                mock.call("run mock_func with positional args = ('1',), "
                          "keyword kwargs = {'y': '2'}, attempt = 2, "
                          "exception = TypeError"),
            ], any_order=False)

            self.assertEqual(mock_func.call_count, 2)
            self.assertEqual(str(error_type.exception), "unexpected")

    def test_error_unexpected_zero_attempts(self):
        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):
            mock_func = mock.Mock(side_effect=ValueError("unexpected"))
            mock_func.__name__ = "mock_func"
            deco_func = parametr_deco(0)(mock_func)

            result = deco_func('1', y='2')

            mock_print.assert_not_called()
            self.assertIsNone(result)
            self.assertEqual(mock_func.call_count, 0)

    def test_expected_exception_message(self):
        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):
            mock_func = mock.Mock(side_effect=ValueError("Custom Message"))
            mock_func.__name__ = "mock_func"
            deco_func = parametr_deco(2, (ValueError,))(mock_func)

            with self.assertRaises(ValueError) as error_type:
                deco_func('1', y='2')

            self.assertEqual(str(error_type.exception), "Custom Message")
            self.assertEqual(mock_print.call_count, 1)

    def test_unexpected_exception_message_after_retries(self):
        mock_print = mock.Mock()

        with mock.patch("builtins.print", mock_print):
            mock_func = mock.Mock(side_effect=TypeError("Another Message"))
            mock_func.__name__ = "mock_func"
            deco_func = parametr_deco(2)(mock_func)

            with self.assertRaises(TypeError) as error_type:
                deco_func('1', y='2')

            mock_print.assert_has_calls([
                mock.call("run mock_func with positional args = ('1',), "
                          "keyword kwargs = {'y': '2'}, attempt = 1, "
                          "exception = TypeError"),
                mock.call("run mock_func with positional args = ('1',), "
                          "keyword kwargs = {'y': '2'}, attempt = 2, "
                          "exception = TypeError"),
            ])

            self.assertEqual(str(error_type.exception), "Another Message")
            self.assertEqual(mock_print.call_count, 2)

    def test_success_after_error(self):
        mock_print = mock.Mock()

        def side_effect(*_args, **_kwargs):
            if side_effect.call_count < 5:
                side_effect.call_count += 1
                raise TypeError("fail")
            return "success"

        side_effect.call_count = 0
        with mock.patch("builtins.print", mock_print):
            mock_func = mock.Mock(side_effect=side_effect)
            mock_func.__name__ = "mock_func"
            deco_func = parametr_deco(6)(mock_func)

            result = deco_func('1', y='2')
            self.assertEqual(result, "success")

            expected_calls = [
                mock.call("run mock_func with positional args = ('1',), "
                          "keyword kwargs = {'y': '2'}, attempt = 1, "
                          "exception = TypeError"),
                mock.call("run mock_func with positional args = ('1',), "
                          "keyword kwargs = {'y': '2'}, attempt = 2, "
                          "exception = TypeError"),
                mock.call("run mock_func with positional args = ('1',), "
                          "keyword kwargs = {'y': '2'}, attempt = 3, "
                          "exception = TypeError"),
                mock.call("run mock_func with positional args = ('1',), "
                          "keyword kwargs = {'y': '2'}, attempt = 4, "
                          "exception = TypeError"),
                mock.call("run mock_func with positional args = ('1',), "
                          "keyword kwargs = {'y': '2'}, attempt = 5, "
                          "exception = TypeError"),
                mock.call("run mock_func with positional args = ('1',), "
                          "keyword kwargs = {'y': '2'}, attempt = 6, "
                          "result = success"),
            ]
            mock_print.assert_has_calls(expected_calls)
            self.assertEqual(mock_print.call_count, 6)

    def test_fail_expected_after_unexpected(self):
        mock_print = mock.Mock()

        def side_effect(*_args, **_kwargs):
            if side_effect.call_count < 3:
                side_effect.call_count += 1
                raise TypeError("fail")
            return "success"

        side_effect.call_count = 0
        with mock.patch("builtins.print", mock_print):
            mock_func = mock.Mock(side_effect=side_effect)
            mock_func.__name__ = "mock_func"
            deco_func = parametr_deco((6), (ValueError,))(mock_func)

            result = deco_func('1', y='2')
            self.assertEqual(result, "success")

            expected_calls = [
                mock.call("run mock_func with positional args = ('1',), "
                          "keyword kwargs = {'y': '2'}, attempt = 1, "
                          "exception = TypeError"),
                mock.call("run mock_func with positional args = ('1',), "
                          "keyword kwargs = {'y': '2'}, attempt = 2, "
                          "exception = TypeError"),
                mock.call("run mock_func with positional args = ('1',), "
                          "keyword kwargs = {'y': '2'}, attempt = 3, "
                          "exception = TypeError"),
                mock.call("run mock_func with positional args = ('1',), "
                          "keyword kwargs = {'y': '2'}, attempt = 4, "
                          "result = success"),
            ]
            mock_print.assert_has_calls(expected_calls)
            self.assertEqual(mock_print.call_count, 4)
