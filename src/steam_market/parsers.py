from bs4 import BeautifulSoup
from requests import Session
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

from core.settings import STEAM_MARKET_URL


def get_currency_rub_usd():
    url = 'https://ru.investing.com/currencies/usd-rub'
    session = Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/39.0.2171.95 Safari/537.36'
    }
    res = session.get(url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    currency_value = soup.find('span', id='last_last')
    return float(currency_value.text.strip().replace(',', '.'))


class SteamParser:
    """Class to parse steam data"""

    url = STEAM_MARKET_URL

    @staticmethod
    def _get_skin_name_to_search(name: str) -> str:
        search_name = (
            name
            .replace(' ', '+').replace('|', '%7C')
            .replace('(', '%28').replace(')', '%29')
        )
        return search_name

    @classmethod
    def get_skin_data(cls, name: str):
        options = Options()
        profile = webdriver.FirefoxProfile()
        profile.set_preference('intl.accept_languages', 'ru-RU')
        browser = webdriver.Firefox(
            options=options, firefox_profile=profile
        )

        currency = get_currency_rub_usd()
        search_name = cls._get_skin_name_to_search(name)
        browser.get(cls.url + search_name)

        try:
            price = float(browser.find_element_by_class_name(
                'normal_price'
            ).text.split()[1].replace('$', '').replace(',', '')) * currency
            price = round(price, 2)
            link = browser.find_element_by_id('resultlink_0').get_attribute('href')
            count = int(browser.find_element_by_class_name(
                'market_listing_num_listings_qty'
            ).get_attribute('data-qty'))
            browser.quit()
        except NoSuchElementException:
            browser.quit()
            price = 0
            link = ''
            count = 0

        return price, link, count
