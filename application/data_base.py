import logging
import sqlite3

import pandas as pd

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - '
           '%(funcName)s: %(lineno)d - %(message)s',
    level=logging.DEBUG)


def main() -> None:
    logging.debug('Applications has been successfully launched.')
    CONN = sqlite3.connect('./data/cards.db')  # Connect to DataBase
    CURSOR = CONN.cursor()  # Create cursor
    CURSOR.execute("""CREATE TABLE IF NOT EXISTS cards(
        INT NUMBER,
        REAL AMOUNT);""")  # Create table
    logging.info('DataBase has been successfully created')
    CONN.commit()  # Commit changes

    # Open file with data
    data = pd.read_excel(r'./data/cards.xlsx', engine='openpyxl')
    records = []

    logging.info('Data has been successfully saved')
    for num, price in zip(data['Number'], data['Amount']):
        records.append((num, price))

    # Add data into the DataBase
    CURSOR.executemany('INSERT INTO cards VALUES(?, ?);', records)
    CONN.commit()

    logging.info('DataBase is created. Data has been recorded.')
    CURSOR.close()


if __name__ == '__main__':
    main()
