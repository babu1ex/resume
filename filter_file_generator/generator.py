def filter_file(  # pylint: disable=dangerous-default-value,too-many-branches
        name,
        filtr_words_lst: list = [],
        stop_words_lst: list = []
):
    try:  # pylint: disable=too-many-nested-blocks
        if isinstance(name, str):
            file = open(name, 'r', encoding='UTF-8')  # pylint: disable=consider-using-with
        else:
            file = name  # Используем файловый объект, если это он
        low_filtr_words_lst = [word.lower() for word in filtr_words_lst]  # Преобразование в нижний регистр один раз
        stop_words_set = set(word.lower() for word in stop_words_lst)
        for string in file:
            count = 0
            low_string = (''.join(char for char in string if char.isalnum() or char.isspace())).lower()
            each_string_set = set(low_string.split())
            if stop_words_set & each_string_set:
                continue
            for filtr_word in low_filtr_words_lst:
                if filtr_word in each_string_set:
                    count += 1
            if count > 0:
                yield string.strip()
    finally:
        if isinstance(name, str):
            file.close()
