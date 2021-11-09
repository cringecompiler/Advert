import json
import keyword


class Base:
    """вспомогательный класс для вывода текста"""
    def __repr__(self):
        return f'{self.title} | {self.price} ₽'


class ColorizeMixin:
    """миксин для изменения цвета вывода в консоль"""
    def __repr__(self):
        ad_text = super().__repr__()
        return f"\033[0;{self.repr_color_code};49m{ad_text}"


class Unpack:
    """класс для распаковки значения атрибута, являющимся словарем"""
    def __init__(self, atr_dict):
        for key, value in atr_dict.items():
            setattr(self, key, value)


class Advert(ColorizeMixin, Base):
    """основной класс"""
    repr_color_code = 33

    def __init__(self, atr_dict):
        self._price = 0
        for key, value in atr_dict.items():
            if keyword.iskeyword(key):  # если название атрибута является ключевым словом
                if type(value) == dict:
                    setattr(self, key + '_', Unpack(value))
            elif type(value) == dict:  # если значение атрибута - словарь
                setattr(self, key, Unpack(value))
            else:
                setattr(self, key, value)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, val):
        if val < 0:  # проверка на неотрицательность значения price
            raise ValueError('price must be >= 0')
        self._price = val


if __name__ == '__main__':
    dog = """{
              "title": "Вельш-корги",
              "price": 1000,
              "class": "dogs",
              "location": {
                "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
              }
            }"""

    phone = """{
              "title": "iPhone X",
              "price": 100,
              "location": {
                "address": "город Самара, улица Мориса Тореза, 50",
                "metro_stations": ["Спортивная", "Гагаринская"]
              }
            }"""
    file_str = phone

    file = json.loads(file_str)
    file_ad = Advert(file)
    print(file_ad.location.address)
    print(file_ad)
