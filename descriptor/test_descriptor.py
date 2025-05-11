import unittest
from descriptor import GameHero
from descriptor import HeroDescriptor


class TestDescriptor(unittest.TestCase):  # pylint: disable=too-many-public-methods

    def test_with_correct_values(self):
        hero = GameHero(50, 20.0, 'Гришаня')
        self.assertEqual(hero.health, 50)
        self.assertEqual(hero.mana, 20.0)
        self.assertEqual(hero.hero_name, 'Гришаня')
        self.assertIn('health', hero.__dict__)
        self.assertIn('mana', hero.__dict__)
        self.assertIn('hero_name', hero.__dict__)

    def test_health_zero(self):
        with self.assertRaisesRegex(ValueError, "Мертвец не может быть героем!"):
            GameHero(0, 20.0, 'Гришаня')

    def test_health_negative(self):
        with self.assertRaisesRegex(ValueError, "Мертвец не может быть героем!"):
            GameHero(-1, 20.0, 'Гришаня')

    def test_health_above_limit(self):
        with self.assertRaisesRegex(ValueError, "Жулик! Очки здоровья не могут превышать 100 единиц!"):
            GameHero(101, 20.0, 'Гришаня')

    def test_health_not_int(self):
        with self.assertRaisesRegex(TypeError, "Очки здоровья могут быть только целочисленным значением!"):
            GameHero('1', 20.0, 'Гришаня')

    def test_mana_negative(self):
        with self.assertRaisesRegex(ValueError, "Герой не может иметь отрицательное кол-во маны!"):
            GameHero(99, -2.0, 'Гришаня')

    def test_mana_above_limit(self):
        with self.assertRaisesRegex(ValueError, "Герой еще не стал феей, чтобы иметь столько маны!"):
            GameHero(99, 55.0, 'Гришаня')

    def test_mana_over_health(self):
        with self.assertRaisesRegex(ValueError, "Очки маны не могу превышать очки здоровья!"):
            GameHero(44, 50.0, 'Гришаня')

    def test_mana_not_float(self):
        with self.assertRaisesRegex(TypeError, "Очки маны могут быть только вещественным числом"):
            GameHero(99, 50, 'Гришаня')

    def test_mana_equals_health(self):
        hero = GameHero(50, 50.0, 'Гришаня')
        self.assertEqual(hero.mana, 50.0)

    def test_name_not_is_alpha(self):
        with self.assertRaisesRegex(ValueError, "Имя героя может состоять только из букв!"):
            GameHero(99, 50.0, 'Гришаня1')

    def test_name_not_is_title(self):
        with self.assertRaisesRegex(ValueError, 'Имя героя должно начинаться с большой буквы!'):
            GameHero(99, 50.0, 'гришаня')

    def test_health_is_one(self):
        hero = GameHero(1, 0.01, 'Гришаня')
        self.assertEqual(hero.health, 1)

    def test_name_empty(self):
        with self.assertRaisesRegex(ValueError, "Имя героя может состоять только из букв!"):
            GameHero(50, 25.0, '')

    def test_descriptor_access_via_class(self):
        self.assertIsNone(GameHero.health)
        self.assertIsNone(GameHero.mana)
        self.assertIsNone(GameHero.hero_name)

    def test_cannot_instantiate_without_validate(self):

        class BrokenDescriptor(HeroDescriptor):  # pylint: disable=too-few-public-methods
            pass

        with self.assertRaises(TypeError):
            BrokenDescriptor()  # pylint: disable=abstract-class-instantiated

    def test_change_to_uncorrect_values(self):
        hero1 = GameHero(health=10, mana=5.5, hero_name="Shrek")

        self.assertEqual(hero1.health, 10)
        self.assertEqual(hero1.mana, 5.5)
        self.assertEqual(hero1.hero_name, "Shrek")

        with self.assertRaisesRegex(ValueError, "Очки маны не могу превышать очки здоровья!"):
            hero1.mana = 20.0

    def test_change_to_correct_values(self):
        hero1 = GameHero(health=100, mana=5.5, hero_name="Shrek")

        self.assertEqual(hero1.health, 100)
        self.assertEqual(hero1.mana, 5.5)
        self.assertEqual(hero1.hero_name, "Shrek")

        hero1.mana = 20.0
        self.assertEqual(hero1.mana, 20.0)

    def test_uncorrect_values_dont_change_default_value_mana(self):
        hero1 = GameHero(health=10, mana=5.5, hero_name="Shrek")

        self.assertEqual(hero1.health, 10)
        self.assertEqual(hero1.mana, 5.5)
        self.assertEqual(hero1.hero_name, "Shrek")

        with self.assertRaisesRegex(ValueError, "Очки маны не могу превышать очки здоровья!"):
            hero1.mana = 20.0

        self.assertEqual(hero1.mana, 5.5)

    def test_uncorrect_values_dont_change_default_value_health(self):
        hero1 = GameHero(health=10, mana=5.5, hero_name="Shrek")

        self.assertEqual(hero1.health, 10)
        self.assertEqual(hero1.mana, 5.5)
        self.assertEqual(hero1.hero_name, "Shrek")

        with self.assertRaisesRegex(ValueError, "Мертвец не может быть героем!"):
            hero1.health = -10

        self.assertEqual(hero1.health, 10)

    def test_uncorrect_values_dont_change_default_value_hero_name(self):
        hero1 = GameHero(health=10, mana=5.5, hero_name="Shrek")

        self.assertEqual(hero1.health, 10)
        self.assertEqual(hero1.mana, 5.5)
        self.assertEqual(hero1.hero_name, "Shrek")

        with self.assertRaisesRegex(ValueError, "Имя героя может состоять только из букв!"):
            hero1.hero_name = 'Shrek2'
        self.assertEqual(hero1.hero_name, "Shrek")
