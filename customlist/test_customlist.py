import unittest
from customlist import CustomList


class TestCustomList(unittest.TestCase):  # pylint: disable=R0904

    def test_add_int(self):
        cl1 = CustomList([1, 2, 3])
        result = cl1 + 5
        self.assertEqual(list(result), list(CustomList([6, 7, 8])))
        self.assertEqual(list(cl1),  list(CustomList([1, 2, 3])))

    def test_add_customlist(self):
        cl1 = CustomList([1, 1, 1])
        cl2 = CustomList([3])
        result = cl1 + cl2
        self.assertEqual(list(result), list(CustomList([4, 1, 1])))
        self.assertEqual(list(cl1), list(CustomList([1, 1, 1])))
        self.assertEqual(list(cl2), list(CustomList([3])))

    def test_init(self):
        cl1 = CustomList([1, 2, 3])
        self.assertEqual(list(cl1), list(CustomList([1, 2, 3])))

        cl2 = CustomList()
        self.assertEqual(list(cl2), list(CustomList([])))

        cl3 = CustomList([1.0, 2.5, 3.7])
        self.assertEqual(list(cl3), list(CustomList([1.0, 2.5, 3.7])))

        self.assertEqual(list(cl1), list(CustomList([1, 2, 3])))
        self.assertEqual(list(cl2), list(CustomList()))
        self.assertEqual(list(cl3), list(CustomList([1.0, 2.5, 3.7])))

    def test_add_with_custom_list_dif_len_self(self):
        list1 = CustomList([1, 2, 3])
        result = list1 + CustomList([6, 7, 8, 9, 20])
        self.assertEqual(list(result), list(CustomList([7, 9, 11, 9, 20])))
        self.assertEqual(list(list1), list(CustomList([1, 2, 3])))

    def test_add_with_custom_list_dif_len_other(self):
        list1 = CustomList([1, 2, 3, 9, 20])
        result = list1 + CustomList([6, 7, 8])
        self.assertEqual(list(result), list(CustomList([7, 9, 11, 9, 20])))
        self.assertEqual(list(list1), list(CustomList([1, 2, 3, 9, 20])))

    def test_add_with_custom_list_one_elem_self(self):
        list1 = CustomList([1])
        result = list1 + CustomList([6, 7, 8])
        self.assertEqual(list(result), list(CustomList([7, 7, 8])))
        self.assertEqual(list(list1), list(CustomList([1])))

    def test_add_with_custom_list_one_elem_other(self):
        list1 = CustomList([6, 7, 8])
        result = list1 + CustomList([1])
        self.assertEqual(list(result), list(CustomList([7, 7, 8])))
        self.assertEqual(list(list1), list(CustomList([6, 7, 8])))

    def test_add_customlist_empty(self):
        cl1 = CustomList([1, 2, 3])
        cl2 = CustomList([])
        result = cl1 + cl2
        self.assertEqual(list(result), list(CustomList([1, 2, 3])))
        self.assertEqual(list(cl1), list(CustomList([1, 2, 3])))
        self.assertEqual(list(cl2), list(CustomList([])))

    def test_add_customlist_with_zeros(self):
        cl1 = CustomList([1, 2, 3])
        cl2 = CustomList([0, 0, 0])
        result = cl1 + cl2
        self.assertEqual(list(result), list(CustomList([1, 2, 3])))
        self.assertEqual(list(cl1), list(CustomList([1, 2, 3])))
        self.assertEqual(list(cl2), list(CustomList([0, 0, 0])))

    def test_radd_with_int(self):
        list1 = CustomList([1, 2, 3])
        result = 5 + list1
        self.assertEqual(list(result), list(CustomList([6, 7, 8])))
        self.assertEqual(list(list1), list(CustomList([1, 2, 3])))

    def test_radd_with_custom_list(self):
        list1 = CustomList([1, 2, 3])
        result = [6, 7, 8] + list1
        self.assertEqual(list(result), list(CustomList([7, 9, 11])))
        self.assertEqual(list(list1), list(CustomList([1, 2, 3])))

    def test_radd_with_custom_list_dif_len_self(self):
        list1 = CustomList([1, 2, 3])
        result = [6, 7, 8, 9, 20] + list1
        self.assertEqual(list(result), list(CustomList([7, 9, 11, 9, 20])))
        self.assertEqual(list(list1), list(CustomList([1, 2, 3])))

    def test_radd_with_custom_list_dif_len_other(self):
        list1 = CustomList([1, 2, 3, 9, 20])
        result = [6, 7, 8] + list1
        self.assertEqual(list(result), list(CustomList([7, 9, 11, 9, 20])))
        self.assertEqual(list(list1), list(CustomList([1, 2, 3, 9, 20])))

    def test_radd_with_custom_list_one_elem_self(self):
        list1 = CustomList([1])
        result = [6, 7, 8] + list1
        self.assertEqual(list(result), list(CustomList([7, 7, 8])))
        self.assertEqual(list(list1), list(CustomList([1])))

    def test_radd_with_custom_list_one_elem_other(self):
        list1 = CustomList([6, 7, 8])
        result = [1] + list1
        self.assertEqual(list(result), list(CustomList([7, 7, 8])))
        self.assertEqual(list(list1), list(CustomList([6, 7, 8])))

    def test_sub_with_int(self):
        list1 = CustomList([1, 2, 3])
        result = list1 - 5
        self.assertEqual(list(result), list(CustomList([-4, -3, -2])))
        self.assertEqual(list(list1), list(CustomList([1, 2, 3])))

    def test_sub_with_custom_list(self):
        list1 = CustomList([1, 2, 3])
        result = list1 - CustomList([6, 7, 8])
        self.assertEqual(list(result), list(CustomList([-5, -5, -5])))
        self.assertEqual(list(list1), list(CustomList([1, 2, 3])))

    def test_sub_with_custom_list_dif_len_self(self):
        list1 = CustomList([1, 2, 3])
        result = list1 - CustomList([6, 7, 8, 9, 20])
        self.assertEqual(list(result), list(CustomList([-5, -5, -5, -9, -20])))
        self.assertEqual(list(list1), list(CustomList([1, 2, 3])))

    def test_sub_with_custom_list_dif_len_other(self):
        list1 = CustomList([1, 2, 3, 9, 20])
        result = list1 - CustomList([6, 7, 8])
        self.assertEqual(list(result), list(CustomList([-5, -5, -5, 9, 20])))
        self.assertEqual(list(list1), list(CustomList([1, 2, 3, 9, 20])))

    def test_sub_with_custom_list_one_elem_self(self):
        list1 = CustomList([1])
        result = list1 - CustomList([6, 7, 8])
        self.assertEqual(list(result), list(CustomList([-5, -7, -8])))
        self.assertEqual(list(list1), list(CustomList([1])))

    def test_sub_with_custom_list_one_elem_other(self):
        list1 = CustomList([6, 7, 8])
        result = list1 - CustomList([1])
        self.assertEqual(list(result), list(CustomList([5, 7, 8])))
        self.assertEqual(list(list1), list(CustomList([6, 7, 8])))

    def test_sub_with_default_list(self):
        list1 = CustomList([1, 2, 3])
        result = list1 - [5]
        self.assertEqual(list(result), list(CustomList([-4, 2, 3])))
        self.assertEqual(list(list1), list(CustomList([1, 2, 3])))

    def test_sub_with__default_list(self):
        list1 = CustomList([1, 2, 3])
        result = list1 - [6, 7, 8]
        self.assertEqual(list(result), list(CustomList([-5, -5, -5])))
        self.assertEqual(list(list1), list(CustomList([1, 2, 3])))

    def test_sub_with_default_list_dif_len_self(self):
        list1 = CustomList([1, 2, 3])
        result = list1 - [6, 7, 8, 9, 20]
        self.assertEqual(list(result), list(CustomList([-5, -5, -5, -9, -20])))
        self.assertEqual(list(list1), list(CustomList([1, 2, 3])))

    def test_sub_with_default_list_dif_len_other(self):
        list1 = CustomList([1, 2, 3, 9, 20])
        result = list1 - [6, 7, 8]
        self.assertEqual(list(result), list(CustomList([-5, -5, -5, 9, 20])))
        self.assertEqual(list(list1), list(CustomList([1, 2, 3, 9, 20])))

    def test_sub_with_default_list_one_elem_self(self):
        list1 = CustomList([1])
        result = list1 - [6, 7, 8]
        self.assertEqual(list(result), list(CustomList([-5, -7, -8])))
        self.assertEqual(list(list1), list(CustomList([1])))

    def test_sub_with_default_list_one_elem_other(self):
        list1 = CustomList([6, 7, 8])
        result = list1 - [1]
        self.assertEqual(list(result), list(CustomList([5, 7, 8])))
        self.assertEqual(list(list1), list(CustomList([6, 7, 8])))

    def test_rsub_with_int(self):
        list1 = CustomList([1, 2, 3])
        result = 5 - list1
        self.assertEqual(list(result), list(CustomList([4, 3, 2])))
        self.assertEqual(list(list1), list(CustomList([1, 2, 3])))

    def test_rsub_with_custom_list(self):
        list1 = CustomList([1, 2, 3])
        result = [6, 7, 8] - list1
        self.assertEqual(list(result), list(CustomList([5, 5, 5])))
        self.assertEqual(list(list1), list(CustomList([1, 2, 3])))

    def test_rsub_with_custom_list_dif_len_self(self):
        list1 = CustomList([1, 2, 3])
        result = [6, 7, 8, 9, 20] - list1
        self.assertEqual(list(result), list(CustomList([5, 5, 5, 9, 20])))
        self.assertEqual(list(list1), list(CustomList([1, 2, 3])))

    def test_rsub_with_custom_list_dif_len_other(self):
        list1 = CustomList([1, 2, 3, 9, 20])
        result = [6, 7, 8] - list1
        self.assertEqual(list(result), list(CustomList([5, 5, 5, -9, -20])))
        self.assertEqual(list(list1), list(CustomList([1, 2, 3, 9, 20])))

    def test_rsub_with_custom_list_one_elem_self(self):
        list1 = CustomList([1])
        result = [6, 7, 8] - list1
        self.assertEqual(list(result), list(CustomList([5, 7, 8])))
        self.assertEqual(list(list1), list(CustomList([1])))

    def test_rsub_with_custom_list_one_elem_other(self):
        list1 = CustomList([6, 7, 8])
        result = [1] - list1
        self.assertEqual(list(result), list(CustomList([-5, -7, -8])))
        self.assertEqual(list(list1), list(CustomList([6, 7, 8])))

    def test_eq_false(self):
        list1 = CustomList([6, 7, 8])
        result = CustomList([1, 2, 3]) == list1
        self.assertEqual(result, False)
        self.assertEqual(list(list1), list(CustomList([6, 7, 8])))

    def test_eq_true(self):
        list1 = CustomList([1, 2, 3])
        result = CustomList([1, 2, 3]) == list1
        self.assertEqual(result, True)
        self.assertEqual(list(list1), list(CustomList([1, 2, 3])))

    def test_ne_false(self):
        list1 = CustomList([6, 7, 8])
        result = CustomList([1, 2, 3]) != list1
        self.assertEqual(result, True)
        self.assertEqual(list(list1), list(CustomList([6, 7, 8])))

    def test_lt_true(self):
        list1 = CustomList([1, 2, 3, 4])
        result = CustomList([1, 2, 3]) < list1
        self.assertEqual(result, True)
        self.assertEqual(list(list1), list(CustomList([1, 2, 3, 4])))

    def test_lt_false(self):
        list1 = CustomList([1, 2, 3])
        result = CustomList([1, 2, 3]) < list1
        self.assertEqual(result, False)
        self.assertEqual(list(list1), list(CustomList([1, 2, 3])))

    def test_le_true(self):
        list1 = CustomList([1, 2, 3, 4])
        result = CustomList([1, 2, 3]) <= list1
        self.assertEqual(result, True)
        self.assertEqual(list(list1), list(CustomList([1, 2, 3, 4])))

    def test_le_true_eq(self):
        list1 = CustomList([1, 2, 3])
        result = CustomList([1, 2, 3]) <= list1
        self.assertEqual(result, True)
        self.assertEqual(list(list1), list(CustomList([1, 2, 3])))

    def test_le_false(self):
        list1 = CustomList([1, 2, 3])
        result = CustomList([1, 2, 3, 4]) <= list1
        self.assertEqual(result, False)
        self.assertEqual(list(list1), list(CustomList([1, 2, 3])))

    def test_gt_false(self):
        list1 = CustomList([1, 2, 5])
        result = CustomList([1, 2, 3]) > list1
        self.assertEqual(result, False)
        self.assertEqual(list(list1), list(CustomList([1, 2, 5])))

    def test_gt_true(self):
        list1 = CustomList([1, 2, 3])
        result = CustomList([1, 2, 3, 1000]) > list1
        self.assertEqual(result, True)
        self.assertEqual(list(list1), list(CustomList([1, 2, 3])))

    def test_ge_true(self):
        list1 = CustomList([1, 2, 3])
        result = CustomList([1, 2, 3, 4]) >= list1
        self.assertEqual(result, True)
        self.assertEqual(list(list1), list(CustomList([1, 2, 3])))

    def test_ge_true_eq(self):
        list1 = CustomList([1, 2, 3, 4])
        result = CustomList([1, 2, 3, 4]) >= list1
        self.assertEqual(result, True)
        self.assertEqual(list(list1), list(CustomList([1, 2, 3, 4])))

    def test_ge_false(self):
        list1 = CustomList([1, 2, 3, 4])
        result = CustomList([1, 2, 3]) >= list1
        self.assertEqual(result, False)
        self.assertEqual(list(list1), list(CustomList([1, 2, 3, 4])))

    def test_str(self):
        expected_string = 'elements: 1, 2, 3, 4; sum : 10'
        self.assertEqual(str(CustomList([1, 2, 3, 4])), expected_string)

    def test_original_list_unchanged_after_add(self):
        cl1 = CustomList([1, 2, 3])
        cl2 = CustomList([4])
        _ = cl1 + cl2
        self.assertEqual(list(cl1), list(CustomList([1, 2, 3])))
        self.assertEqual(list(cl2), list(CustomList([4])))

    def test_eq_same_sum_different_elements(self):
        cl1 = CustomList([1, 2, 3])
        cl2 = CustomList([0, 3, 3])
        self.assertEqual(cl1 == cl2, True)
        self.assertEqual(list(cl1), list(CustomList([1, 2, 3])))
        self.assertEqual(list(cl2), list(CustomList([0, 3, 3])))

    def test_eq_different_sum(self):
        cl1 = CustomList([1, 2, 3])
        cl2 = CustomList([1, 2, 4])
        self.assertEqual(cl1 == cl2, False)
        self.assertEqual(list(cl1), list(CustomList([1, 2, 3])))
        self.assertEqual(list(cl2), list(CustomList([1, 2, 4])))
