class CustomList(list):

    def __init__(self, value: list[int] | None = None):
        if value is None:
            value = []
        super().__init__(value)

    def __add__(self, other):
        result = []
        if isinstance(other, int):
            for i, val1 in enumerate(self):
                result.append(other + val1)
            return CustomList(result)
        max_len = max(len(self), len(other))
        for i in range(max_len):
            val1 = self[i] if i < len(self) else 0  # 0 для отсутствующих элементов
            val2 = other[i] if i < len(other) else 0   # 0 для отсутствующих элементов
            result.append(val1 + val2)
        return CustomList(result)

    def __radd__(self, other):
        result = []
        if isinstance(other, int):
            for i, val1 in enumerate(self):
                result.append(other + val1)
            return CustomList(result)
        max_len = max(len(self), len(other))
        for i in range(max_len):
            val1 = self[i] if i < len(self) else 0  # 0 для отсутствующих элементов
            val2 = other[i] if i < len(other) else 0   # 0 для отсутствующих элементов
            result.append(val2 + val1)
        return CustomList(result)

    def __sub__(self, other):
        result = []
        if isinstance(other, int):
            for i, val1 in enumerate(self):
                result.append(val1 - other)
            return CustomList(result)
        max_len = max(len(self), len(other))
        for i in range(max_len):
            val1 = self[i] if i < len(self) else 0  # 0 для отсутствующих элементов
            val2 = other[i] if i < len(other) else 0   # 0 для отсутствующих элементов
            result.append(val1 - val2)
        return CustomList(result)

    def __rsub__(self, other):
        result = []
        if isinstance(other, int):
            for i, val1 in enumerate(self):
                result.append(other - val1)
            return CustomList(result)
        max_len = max(len(self), len(other))
        for i in range(max_len):
            val1 = self[i] if i < len(self) else 0  # 0 для отсутствующих элементов
            val2 = other[i] if i < len(other) else 0   # 0 для отсутствующих элементов
            result.append(val2 - val1)
        return CustomList(result)

    def __eq__(self, other: 'CustomList', /):
        return sum(self) == sum(other)

    def __ne__(self, other: 'CustomList', /):
        return sum(self) != sum(other)

    def __lt__(self, other: 'CustomList', /):
        return sum(self) < sum(other)

    def __le__(self, other: 'CustomList', /):
        return sum(self) <= sum(other)

    def __gt__(self, other: 'CustomList', /):
        return sum(self) > sum(other)

    def __ge__(self, other: 'CustomList', /):
        return sum(self) >= sum(other)

    def __str__(self, /):
        return f"elements: {', '.join(map(str, self))}; sum : {sum(self)}"
