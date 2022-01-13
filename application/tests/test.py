import unittest

import requests
from bs4 import BeautifulSoup as bs


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

    def test_status_code(self):
        response = requests.get(self.URL, headers=self.USER_AGENT)
        self.assertEqual(response.status_code, 200)

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


if __name__ == '__main__':
    unittest.main()
