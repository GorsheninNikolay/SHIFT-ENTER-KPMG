# SHIFT-ENTER-KPMG

### Направление «Python-разработчик», KPMG

Задание 1. Напиши программу для парсинга данных
--------------------------------------------------------------------------------------

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

Решение
--------------

Файл - ``main.py``

Документация по коду:

1. Импортируем нужные библиотеки для парсинга

```python
import logging

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
```

2. Создаем дочерний класс от ``Exception``, а также задаем конфиг для логгирования

```python
class WrongResponse(Exception):
    pass


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - '
           '%(funcName)s: %(lineno)d - %(message)s',
    level=logging.DEBUG)
```

3. Приложение начинает работать с функции main, где было использовано разделение

```python
if __name__ == '__main__':
    main()
```

4. Для начала логгируем запуск приложения, создаем переменную ``url`` с динамической переменной page для сбора данных вместе с пагинацией, а также переменную ``data`` для сохранения информации. ``USER_AGENT`` служит для обхода блокировок во время парсинга.

```python
logging.debug('Applications has been successfully launched.')
USER_AGENT = {'User-agent': 'Mozilla/5.0'}
url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=&morphology=on&search-filter=Дате+размещения&pageNumber={page}&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&savedSearchSettingsIdHidden=&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&placingWayList=&selectedLaws=&priceFromGeneral=&priceFromGWS=&priceFromUnitGWS=&priceToGeneral=&priceToGWS=&priceToUnitGWS=&currencyIdGeneral=-1&publishDateFrom=&publishDateTo=&applSubmissionCloseDateFrom=&applSubmissionCloseDateTo=&customerIdOrg=&customerFz94id=&customerTitle=&okpd2Ids=&okpd2IdsCodes=&gws='  # noqa
data = {}
```

5. Используя библиотеку ``requests``, отправляем get запрос на сайт и проверяем, что статус-код - 200, что дает нам уверенность в работе сайта

```python
response = requests.get(url=url.format(page='1'),
                            headers=USER_AGENT,
                            timeout=10)

# Check response code
if not response.ok:
    logging.error('Status code is not equal 200 — problem in loading site')
    raise WrongResponse(
        'Status code is not equal 200 — problem in loading site'
    )
```

6. Используя библиотеку ``BeautifulSoup``, при помощи цикла на каждой итерации находим блок ``registry-entry__header-mid__number``, который содержит номера закупок, а также ``price-block__value``, который содержит стоимость закупки. В конце итерации сохраняем полученные данные.

```python
# Iteration for saving data
for page in range(2, 101):
    response = requests.get(
        url=url.format(page=str(page)),
        headers=USER_AGENT,
        timeout=10
    )
    soup = bs(response.text, 'html.parser')

    blocks_numbers = soup.find_all(
        'div',
        class_='registry-entry__header-mid__number'
    )

    blocks_prices = soup.find_all('div', class_='price-block__value')

    for x, y in zip(blocks_numbers, blocks_prices):
        data[x.text.strip().split()[-1]] = convert_price(y.text.strip())
```

P.S: Преобразование суммы закупок затруднительно, так как используются элементы оформления. Чтобы правильно преобразовать сумму в число типа float, я использовал функцию ``convert_price``

```python
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

7. Последний шаг - преобразование данных для записи в таблицу Excel

```python
df = pd.DataFrame(
        {
            'Number': [int(num) for num in data.keys()],
            'Amount': [price for price in data.values()]
        }
    )

df.to_excel('cards.xlsx')
```

Задание 2. Напиши юнит-тест для проверки своей программы
------------------------------------------------------------------------------------------------------

Чуть позже ты получил письмо от руководителя с новым заданием. Подход
TDD (разработка через тестирование) хорошо подходит для
юнит-тестирования. Так как твой код еще не покрыт тестами, руководитель
отказывается принимать твою задачу. Возможно, в твоем решении есть баги,
и оно не полностью работоспособно, поэтому твоя задача — написать
юнит-тест, который протестирует алгоритм работы программы парсинга.

```
Привет!
Спасибо за твое решение! Чтобы мы с коллегами смогли взять твой код в работу, тебе
нужно написать юнит-тест на Python для тестирования своей программы.
Юнит-тест представляет собой программу, проверяющую работу небольшой части кода.
Разработчики регулярно обновляют ПО и вносят правки, поэтому существуют разные типы
тестов. Представь пирамиду с основанием в виде юнит-тестов, далее следует слой с
интеграционными тестами, затем — системные тесты, и на вершине пирамиды находятся
end-to-end тесты. Обычно при разработке программы программист пишет юнит-тесты, а
далее тестировщик пишет все остальные виды тестов. Но без юнит-тестов невозможен в
целом механизм полного тестирования приложения: написание этих тестов является
основой для других тестов, без них невозможно 100%-е покрытие кода тестами.
Юнит-тесты могут быть написаны с нуля без использования библиотек, однако проще
воспользоваться уже готовыми фреймворками. В Python их несколько, но я предлагаю
поработать с unittest. Шаблон структуры юнит-теста дан во вложении 2.
Тебе нужно:
1. Как и в предыдущем задании, считать данные с сайта госзакупок и сохранить их
в удобном формате.
2. Провести проверку на успешность с помощью функции assertGreater, чтобы
выбрать все ненулевые данные.
3. Провести еще одну проверку на успешность, используя assertIsNotNone для
аргументов с номером карточки и ценой.
Оформи свое решение в виде файла Python и пришли мне его через час. Спасибо!
```

Решение
--------------

Файл - ``test.py``

1. Импортируем нужные библиотеки

```python
import unittest

import requests
from bs4 import BeautifulSoup as bs
```

2. Создаем дочерний класс ``TestParsing`` от класса ``unittest.TestCase``, также константы USER_AGENT и URL

```python
class TestParsing(unittest.TestCase):
    USER_AGENT = {'User-agent': 'Mozilla/5.0'}
    URL = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html'
    '?searchString=&morphology=on&search-filter=Дате+размещения&'
    'pageNumber=1&sortDirection=false&recordsPerPage=_10'
    '&showLotsInfoHidden=false&savedSearchSettingsIdHidden='
    '&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on'
    '&placingWayList=&selectedLaws=&priceFromGeneral=&priceFromGWS'
    '=&priceFromUnitGWS=&priceToGeneral=&priceToGWS=&priceToUnitGWS=&'
    'currencyIdGeneral=-1&publishDateFrom=&publishDateTo=&applSubmissio'
    'nCloseDateFrom=&applSubmissionCloseDateTo=&customerIdOrg=&custome'
    'rFz94id=&customerTitle=&okpd2Ids=&okpd2IdsCodes=&gws='
```

3. Внутри класса ``TestParsing`` создаем тест-фукнцию для проверки статус кода

```python
def test_status_code(self):
        response = requests.get(self.URL, headers=self.USER_AGENT)
        self.assertEqual(response.status_code, 200)
```

4. Внутри класса ``TestParsing`` создаем тест-функцию для проверки наличия записей

```python
def test_records(self):
    response = requests.get(self.URL, headers=self.USER_AGENT)
    soup = bs(response.text, 'html.parser')
    blocks_numbers = soup.find_all(
        'div',
        class_='registry-entry__header-mid__number'
    )

    blocks_prices = soup.find_all('div', class_='price-block__value')
    self.assertIsNotNone(blocks_numbers)
    self.assertIsNotNone(blocks_prices)
    self.assertGreater(len(blocks_prices), 0)
```


Задание 3. Создай базу данных по закупкам и напиши юнит-тест по ее проверке
-----

Чуть позже ты получил сообщение от руководителя в мессенджере с постановкой финального на сегодня задания.

```
Привет!
Спасибо за отлично проделанную работу. Запуск файла с юнит-тестом для программы
парсинга прошел успешно и без ошибок. Теперь тебе осталось сделать всего одну задачу —
спроектировать базу данных по закупкам и проверить ее работу при помощи юнит-теста.
Первым этапом проектирования БД станет создание таблицы cards. Обычно для создания БД
SQLite в Python используется объект Connection, который создается с помощью функции
connect библиотеки sqlite3. Далее нужно создать саму таблицу cards, содержащую 2
колонки — number и amount, в которых находятся номер закупки и начальная цена объекта.
Для твоего удобства интересующие нас значения уже импортированы с портала госзакупок в
виде таблицы (см. вложение 3).
Hints: для добавления данных нужно использовать объект cursor и функцию executemany для
выборки нескольких значений из БД. Подробно об этом написано в руководстве по SQLite,
ссылка на которое дана во вкладке «Полезные материалы». Для выборки данных из БД не
забудь использовать fetchall, а также проверить, что данные действительно выбрались с
помощью команды print.
После этого напиши в отдельном Python-файле юнит-тест для проверки работы БД, как ты
делал это для программы парсинга. Здесь важно написать запрос для выбора первых трех
строк, а также проверки на успешность, связанные с проверкой того, что значения
заполнены и не пустые (assertIsNot(x, 0) и assertGreater(x, 0)).
Как обычно, оформи свое решение в виде папки с файлами (Python-файлы и README).
Жду твое решение, спасибо за помощь!
```

Решение. Создание базы данных
-----

Файл - data_base.py

1. Импортируем библиотеки
``` python
import logging
import sqlite3

import pandas as pd
```
2. Задаем конфиг для логгирование
``` python
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - '
           '%(funcName)s: %(lineno)d - %(message)s',
    level=logging.DEBUG)
```
3. Логгируем запуск, подключаемся/создаем базу данных, устанавлиаем курсор для запросов
``` python
logging.debug('Applications has been successfully launched.')
CONN = sqlite3.connect('./data/cards.db')  # Connect to DataBase
CURSOR = CONN.cursor()  # Create cursor
```

4. Создаем таблицу, логгируем результат и сохраняем изменения
``` python
CURSOR.execute("""CREATE TABLE IF NOT EXISTS cards(
        INT NUMBER,
        REAL AMOUNT);""")  # Create table
logging.info('DataBase has been successfully created')
CONN.commit()  # Commit changes
```

5. Открываем Excel файл с данными и сохраняем все в переменную ```records```
``` python
# Open file with data
data = pd.read_excel(r'./data/cards.xlsx', engine='openpyxl')
records = []

logging.info('Data has been successfully saved')
for num, price in zip(data['Number'], data['Amount']):
    records.append((num, price))
```

6. Добавляем в базу данных полученную информацию с парсинга, логгируем результат и закрываем курсор
``` python
# Add data into the DataBase
CURSOR.executemany('INSERT INTO cards VALUES(?, ?);', records)
CONN.commit()

logging.info('DataBase is created. Data has been recorded.')
CURSOR.close()
```


Решение. Тест базы данных
-----
