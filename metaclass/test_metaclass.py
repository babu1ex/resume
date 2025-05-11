# pylint: disable=no-member
import unittest
from metaclass import CustomClass


class TestMetaClass(unittest.TestCase):

    def setUp(self):
        self.obj = CustomClass()

    def test_class_attributes_renamed(self):
        self.assertFalse(hasattr(CustomClass, 'x'))
        self.assertTrue(hasattr(CustomClass, 'custom_x'))
        self.assertEqual(CustomClass.custom_x, 50)
        self.assertTrue(hasattr(self.obj, 'custom_x'))
        self.assertEqual(self.obj.custom_x, 50)

    def test_method_renamed(self):
        self.assertFalse(hasattr(self.obj, 'line'))
        self.assertTrue(hasattr(self.obj, 'custom_line'))
        self.assertEqual(self.obj.custom_line(), 100)

    def test_instance_attribute_set_in_init(self):
        self.assertTrue(hasattr(self.obj, 'custom_val'))
        self.assertEqual(self.obj.custom_val, 99)

    def test_instance_attribute_set_later(self):
        self.obj.new_attr = 'hello'
        self.assertTrue(hasattr(self.obj, 'custom_new_attr'))
        self.assertEqual(self.obj.custom_new_attr, 'hello')

    def test_class_attribute_set_later(self):
        CustomClass.new = 4
        self.assertTrue(hasattr(CustomClass, 'custom_new'))
        self.assertEqual(CustomClass.custom_new, 4)

    def test_str_method_preserved(self):
        self.assertEqual(str(self.obj), 'Custom_by_metaclass')

    def test_magic_methods_not_renamed(self):
        self.assertTrue(hasattr(CustomClass, '__str__'))
        self.assertFalse(hasattr(CustomClass, 'custom___str__'))

    def test_original_names_absent(self):
        self.assertFalse(hasattr(self.obj, 'val'))
        self.assertFalse(hasattr(CustomClass, 'line'))

    def test_instance_attribute_reassignment(self):
        self.obj.val = 123
        self.assertEqual(self.obj.custom_val, 123)
        self.obj.val = 456
        self.assertEqual(self.obj.custom_val, 456)

    def test_inheritance_from_custom_class(self):

        class SubClass(CustomClass):
            y = 200

            def sub_method(self):
                return "sub"

        sub_obj = SubClass()
        self.assertTrue(hasattr(SubClass, 'custom_y'))
        self.assertTrue(hasattr(sub_obj, 'custom_sub_method'))
        self.assertEqual(sub_obj.custom_sub_method(), 'sub')

    def test_init_not_renamed(self):
        self.assertTrue(hasattr(self.obj, '__init__') or '__init__' in dir(self.obj))
        self.assertFalse(hasattr(self.obj, 'custom___init__'))

    def test_no_original_and_custom_name_simultaneously(self):
        self.assertFalse('val' in self.obj.__dict__)
        self.obj.val = 77
        self.assertFalse('val' in self.obj.__dict__)
        self.assertTrue('custom_val' in self.obj.__dict__)

    def test_access_to_old_names_raises(self):
        with self.assertRaises(AttributeError):
            _ = self.obj.val

        with self.assertRaises(AttributeError):
            _ = self.obj.line()

        with self.assertRaises(AttributeError):
            _ = self.obj.x

        with self.assertRaises(AttributeError):
            _ = CustomClass.x

        with self.assertRaises(AttributeError):
            _ = self.obj.dynamic

    def test_class_custom_attr_set_value(self):
        CustomClass.new = 4
        self.assertEqual(CustomClass.custom_new, 4)

    def test_custom_attrs_in_dir(self):
        dir_obj = dir(self.obj)
        self.assertIn('custom_val', dir_obj)
        self.assertIn('custom_line', dir_obj)
        self.assertNotIn('val', dir_obj)
        self.assertNotIn('line', dir_obj)

    def test_values_of_custom_attributes(self):
        self.assertEqual(self.obj.custom_val, 99)
        self.assertEqual(CustomClass.custom_x, 50)
        self.assertEqual(self.obj.custom_x, 50)
        self.assertEqual(self.obj.custom_line(), 100)

    def test_setattr_not_rename_magic(self):
        self.obj.__magic__ = 'value'
        self.assertIn('__magic__', self.obj.__dict__)
        self.assertEqual(self.obj.__dict__['__magic__'], 'value')
        self.assertNotIn('custom___magic__', self.obj.__dict__)
