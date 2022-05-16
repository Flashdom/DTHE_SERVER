# import json
import re

text = """
Давно выяснено, что при оценке дизайна и композиции читаемый текст мешает сосредоточиться. Lorem Ipsum используют потому, что тот обеспечивает более или менее стандартное заполнение шаблона, а также реальное распределение букв и пробелов в абзацах, которое не получается при простой дубликации "Здесь ваш текст.. Здесь ваш текст.. Здесь ваш текст.." Многие программы электронной вёрстки и редакторы HTML используют Lorem Ipsum в качестве текста по умолчанию, так что поиск по ключевым словам "lorem ipsum" сразу показывает, как много веб-страниц всё ещё дожидаются своего настоящего рождения. За прошедшие годы текст Lorem Ipsum получил много версий. Некоторые версии появились по ошибке, некоторые - намеренно (например, юмористические варианты).
"""

lst_no = ['.', ',', ':', '!', '"', "'", '[', ']', '-', '—', '(', ')'  ]   # и т.д.
lst = []

for word in text.lower().split():
    if not word in lst_no:
        _word = word 
        if word[-1] in lst_no:
            _word = _word[:-1]
        if word[0] in lst_no:
            _word = _word[1:] 
        lst.append(_word)

_dict = dict()
for word in lst:
    _dict[word] = _dict.get(word, 0) + 1

# сортируем словарь посредством формирования списка (значение, ключ)
_list = []
for key, value in _dict.items():
    _list.append((value, key))
    _list.sort(reverse=True)

# печатаем первые 10 самых используемых слов
print('Первые 10 самых используемых слов:')
for freq, word in _list[0:3]:
    print(f'{word:>3} -> {freq:>3}')

# print('\nили так: (с условием, что длина слова > 4- букв) \n')
# _dict = {(i, lst.count(i)) for i in lst}
# _list = []

# for word, kol in _dict:
#     _list.append((kol, word))
#     _list.sort(reverse=True)
    
# for freq, word in _list[0:20]:
#     if len(word) > 4:
#         print('{0:10} {1}'.format (word, freq))