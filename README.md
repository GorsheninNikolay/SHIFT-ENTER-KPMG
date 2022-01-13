# SHIFT-ENTER-KPMG 
### Направление «Python-разработчик», KPMG

Задание 1. Напиши программу для парсинга данных
---
Утром ты получил письмо от своего руководителя. Он просит тебя
подключиться к работе по написанию программы для парсинга.
``` 
Привет! KPMG хочет оценить возможности по проникновению на новые рынки. Мы думаем, что анализ
информации портала госзакупок поможет лучше понять условия проведения тендеров.
Поэтому тебе нужно научиться парсить сайт госзакупок с использованием языка
программирования Python (версии 3 и выше) и дополнительной библиотеки для парсинга
сайтов. Некоторые разработчики используют регулярные выражения или встроенные
библиотеки Python, но использование специализированных библиотек для парсинга сайтов —
более удобный метод извлечения информации.
Чтобы создать заготовку для программы парсинга на Python, прошу тебя:
1. Определить, какие библиотеки Python будут нужны для реализации программы.
Hints: обязательно прочитай статьи во вкладке «Полезные материалы».
2. Написать программу получения информации с сайта госзакупок, которая считывала
бы данные и сохраняла их в удобном для дальнейшей работы формате. Для лучшего
понимания структуры HTML-страницы в современных браузерах код можно посмотреть,
кликнув правой кнопкой на странице и нажав «Просмотреть исходный код» (или
комбинацию клавиш Ctrl + U).
Код также должен выводить номер закупки и начальную цену (см. вложение 1).
Hints: для этого используй функцию find и HTML-код из вложения 1.
Оформи свое решение в виде папки с файлами. Не забудь приложить README-файл с
описанием того, что содержится в каждом файле. Пожалуйста, пришли мне архив в
ближайшие полтора часа.
До связи!
```

Решение:

Основной файл - ```main.py```


Документация по коду:
1. Импортируем нужные библиотеки для парсинга
``` python
import logging

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
```
2. Создаем дочерний класс от ```Exception```, а также задаем конфиг для логгирования
``` python
class WrongResponse(Exception):
    pass


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - "
           "%(funcName)s: %(lineno)d - %(message)s",
    level=logging.DEBUG)
```
3. Приложение начинает работать с функции main, где было использовано разделение
```python 
if __name__ == '__main__':
    main()
```
4. Для начала логгируем запуск приложения, создаем переменную ```url``` с динамической переменной page для сбора данных вместе с пагинацией, а также переменную ```data``` для сохранения информации
``` python
logging.debug('Applications has been successfully launched.')
url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=&morphology=on&search-filter=Дате+размещения&pageNumber={page}&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&savedSearchSettingsIdHidden=&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&placingWayList=&selectedLaws=&priceFromGeneral=&priceFromGWS=&priceFromUnitGWS=&priceToGeneral=&priceToGWS=&priceToUnitGWS=&currencyIdGeneral=-1&publishDateFrom=&publishDateTo=&applSubmissionCloseDateFrom=&applSubmissionCloseDateTo=&customerIdOrg=&customerFz94id=&customerTitle=&okpd2Ids=&okpd2IdsCodes=&gws='
data = {}
```
5. Используя библиотеку ```requests```, отправляем get запрос на сайт и проверяем, что статус-код - 200, что дает нам уверенность в работе сайта
``` python
response = requests.get(url=url.format(page='1'), timeout=20)

if not response.ok:
    logging.error('Status code is not equal 200 — problem in loading site')
    raise WrongResponse(
        'Status code is not equal 200 — problem in loading site'
    )
```
6. Используя библиотеку ```BeautifulSoup```, при помощи цикла на каждой итерации находим блок ```registry-entry__header-mid__number```, который содержит номера закупок, а также ```price-block__value```, который содержит стоимость закупки. В конце итерации сохраняем полученные данные.
``` python
for page in range(2, 101):
    response = requests.get(
        url=url.format(page=str(page)), timeout=20
    )
    soup = bs(response.text, 'html.parser')

    block_numbers = soup.find_all(
        'div',
        class_='registry-entry__header-mid__number'
    )

    blocks_prices = soup.find_all('div', class_='price-block__value')

    for x, y in zip(block_numbers, blocks_prices):
        data[x.text.strip().split()[-1]] = convert_price(y.text.strip())
```
P.S: Преобразование суммы закупок затруднительно, так как используются элементы красивого оформления. Чтобы правильно преобразовать сумму в число типа float, я использовал функцию ```convert_price```
``` python
def convert_price(text: str) -> float:
    """This function convert text into the float number"""
    number = ''
    needs = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ','}

    for sym in text:
        if sym in needs:
            if sym == ',':
                number += '.'
            else:
                number += sym

    return float(number)
```
7. Последний шаг - преобразование данных для записи в таблицу Excel для более удобной работы с данными
``` python
df = pd.DataFrame(
        {
            'Number': [int(num) for num in data.keys()],
            'Amount': [price for price in data.values()]
        }
    )

df.to_excel('cards.xlsx')
```
