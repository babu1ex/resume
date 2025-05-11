class CustomMeta(type):
    def __new__(mcs, name, bases, attrs):
        keys_to_rename = [key for key in attrs if not (key.startswith('__') and key.endswith('__'))]
        for key in keys_to_rename:
            attrs[f'custom_{key}'] = attrs.pop(key)

        # __setattr__ для экземпляров класса
        def __setattr__(self, name, value):
            if not (name.startswith('__') and name.endswith('__')):
                object.__setattr__(self, f'custom_{name}', value)
            else:
                object.__setattr__(self, name, value)
        attrs['__setattr__'] = __setattr__

        return super().__new__(mcs, name, bases, attrs)

    def __setattr__(cls, name, value):
        if not (name.startswith('__') and name.endswith('__')):
            name = f'custom_{name}'
        super().__setattr__(name, value)


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"
