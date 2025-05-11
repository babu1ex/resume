from abc import ABC, abstractmethod


class HeroDescriptor(ABC):

    def __set_name__(self, owner, name):
        self.name = name  # pylint: disable=attribute-defined-outside-init

    def __get__(self, obj, objtype):
        if obj is None:
            return None
        return obj.__dict__[self.name]

    def __set__(self, obj, val):
        self.validate(obj, val)
        obj.__dict__[self.name] = val

    @abstractmethod
    def validate(self, obj, value: int | float | str):
        pass


class Health(HeroDescriptor):  # pylint: disable=too-few-public-methods

    def validate(self, obj, value: int):
        if not isinstance(value, int):
            raise TypeError("Очки здоровья могут быть только целочисленным значением!")
        if value <= 0:
            raise ValueError("Мертвец не может быть героем!")
        if value > 100:
            raise ValueError("Жулик! Очки здоровья не могут превышать 100 единиц!")


class Mana(HeroDescriptor):  # pylint: disable=too-few-public-methods

    def validate(self, obj, value: float):
        if not isinstance(value, float):
            raise TypeError("Очки маны могут быть только вещественным числом")
        if value <= 0:
            raise ValueError("Герой не может иметь отрицательное кол-во маны!")
        if value > 50:
            raise ValueError("Герой еще не стал феей, чтобы иметь столько маны!")
        if hasattr(obj, 'health') and value > obj.health:
            raise ValueError("Очки маны не могу превышать очки здоровья!")


class HeroName(HeroDescriptor):  # pylint: disable=too-few-public-methods

    def validate(self, obj, value: str):
        if not value.isalpha():
            raise ValueError("Имя героя может состоять только из букв!")
        if not value.istitle():
            raise ValueError('Имя героя должно начинаться с большой буквы!')


class GameHero:  # pylint: disable=too-few-public-methods

    hero_name = HeroName()
    health = Health()
    mana = Mana()

    def __init__(self, health, mana, hero_name):
        self.health = health
        self.mana = mana
        self.hero_name = hero_name


class BrokenDescriptor(HeroDescriptor):  # pylint: disable=abstract-method,too-few-public-methods
    pass


class BrokenHero:  # pylint: disable=too-few-public-methods
    broken = None
