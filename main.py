import logging

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs


class WrongResponse(Exception):
    pass


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - "
           "%(funcName)s: %(lineno)d - %(message)s",
    level=logging.DEBUG)


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


def main() -> None:
    """
    The main entry point of the application
    """
    logging.debug('Applications has been successfully launched.')
    url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=&morphology=on&search-filter=Дате+размещения&pageNumber={page}&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&savedSearchSettingsIdHidden=&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&placingWayList=&selectedLaws=&priceFromGeneral=&priceFromGWS=&priceFromUnitGWS=&priceToGeneral=&priceToGWS=&priceToUnitGWS=&currencyIdGeneral=-1&publishDateFrom=&publishDateTo=&applSubmissionCloseDateFrom=&applSubmissionCloseDateTo=&customerIdOrg=&customerFz94id=&customerTitle=&okpd2Ids=&okpd2IdsCodes=&gws='
    data = {}

    response = requests.get(url=url.format(page='1'), timeout=20)

    if not response.ok:
        logging.error('Status code is not equal 200 — problem in loading site')
        raise WrongResponse(
            'Status code is not equal 200 — problem in loading site'
        )

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

    df = pd.DataFrame(
        {
            'Number': [int(num) for num in data.keys()],
            'Amount': [price for price in data.values()]
        }
    )

    df.to_excel('cards.xlsx')


if __name__ == '__main__':
    main()
