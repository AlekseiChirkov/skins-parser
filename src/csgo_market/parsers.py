import os
import time

from requests.exceptions import SSLError
from bs4 import BeautifulSoup

from core.settings import CSGO_MARKET_URL, SESSION
from csgo_market.file_writer import FileWriter
from csgo_market.models import CSGOMarketURL
from csgo_market.validators import ParsedDataValidator


class CSGOMarketFilteredPagesParser:
    """Class to parse csgo market"""
    market = CSGOMarketURL

    @classmethod
    def _get_filtered_items_pages_count(
            cls, price_range: str, stickers: str
    ) -> int:
        """
        Method returns total pages count of filtered skins
        :param price_range: string with price range (100;1000)
        :param stickers: string with stickers existence (0, 1)
        :return: int value of pages count
        """

        market = cls.market(price_range=price_range, stickers=stickers)
        url = market.url
        res = SESSION.get(url)
        page = BeautifulSoup(res.content, 'html.parser')

        try:
            total_pages_count = page.find('span', id='total_pages')
            total_pages_count = total_pages_count.text.strip().replace(" ", "")
            return int(total_pages_count)
        except AttributeError:
            return 0

    @classmethod
    def _get_all_pages_links(cls, price_range: str, stickers: str) -> list:
        """
        Method returns list of filtered pages urls
        :param price_range: string with price range (100;900)
        :param stickers: string with stickers existence (0 or 1)
        :return: list with links strings
        """

        pages_count = cls._get_filtered_items_pages_count(
            price_range, stickers
        )

        urls = []
        for page in range(1, pages_count + 1):
            market = cls.market(
                page=str(page), price_range=price_range, stickers=stickers
            )
            urls.append(market.url)

        return urls

    @staticmethod
    def _parse_page(url: str, index: int) -> None:
        """
        Method processes page from url
        :param url: string with page url
        :param index: index of file (will be used to generate file name)
        :return: None
        """

        try:
            res = SESSION.get(url)
            page = BeautifulSoup(res.content, 'html.parser')
            writer = FileWriter()
            writer.write_data_to_txt_file(page, index, '../pages')
        except (SSLError, AttributeError):
            raise SSLError('Too many requests!')

    @classmethod
    def get_all_pages_to_process(cls, price_range: str, stickers: str) -> None:
        """
        Method process all filtered page and return list of html pages
        :param price_range: string with price range (100;900)
        :param stickers: string stickers existence (0 or 1)
        :return: None
        """

        links = cls._get_all_pages_links(price_range, stickers)

        for index, link in enumerate(links):
            cls._parse_page(link, index + 1)


class SkinsParser(ParsedDataValidator):
    """Class to parse skins data"""

    skin_pages = list()

    @staticmethod
    def _get_skins_links() -> list:
        """
        Method returns skin's page links in list
        :return: list with links
        """

        pages = os.listdir('../pages')
        skins_links = []
        for page in pages:
            with open('../pages/' + page, 'r') as file:
                soup = BeautifulSoup(file, 'html.parser')
                skins_block = soup.find('div', id='applications')
                skins = skins_block.find_all('a', class_='item')

                for skin in skins:
                    exclude_item = skin.find('div', class_='name')
                    if "Тренировки по киберспорту" in exclude_item.text:
                        continue
                    skins_links.append(CSGO_MARKET_URL + str(skin.get('href')))

        return skins_links

    @classmethod
    def _get_skins_pages(cls) -> list:
        """
        Method returns skin's pages in list
        :return: list of tuples with skin's page and link
        """

        writer = FileWriter()
        skin_links = cls._get_skins_links()
        print("Links count:", len(skin_links))

        processed_pages = []
        for index, link in enumerate(skin_links):
            time.sleep(0.3)
            res = SESSION.get(link)
            print(f"Page #{index + 1}", res)
            soup = BeautifulSoup(res.content, 'html.parser')
            page = writer.write_data_to_txt_file(
                soup, index + 1, '../skins_pages'
            )
            processed_pages.append((page, link))

        return processed_pages

    @classmethod
    def _process_data(cls, data: list, skins_data: list) -> list:
        """
        Method process data and returns all skin data
        :param data: list with data to process (page(file_path), link)
        :param skins_data: empty list to write in all data
        :return: list with processed data
        """
        
        page = data[0]
        link = data[1]
        with open(page, 'r') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            skin_name = cls.validate_skin_name(soup)
            skin_quality = cls.validate_skin_quality(soup)
            skin_full_name = (
                    skin_name.strip() + ' (' + skin_quality.strip() + ')'
            )
            current_price = float(cls.validate_current_skin_price(soup))
            auto_buy_price = float(cls.validate_auto_buy_skin_price(soup))
            price_difference = current_price - auto_buy_price
            recommended_price = (
                    current_price - (current_price * 0.1)
            )

            skins_data.append(
                [
                    skin_full_name, current_price, auto_buy_price,
                    round(price_difference, 2), recommended_price, link
                ]
            )

        return skins_data

    @classmethod
    def get_skins_data(cls) -> list:
        """
        Method process skin page and returning all skin data
        :return: list of tuples with skin's data
        """

        items = cls._get_skins_pages()

        skins_data = []
        processed_data = []
        for item in items:
            processed_data = cls._process_data(item, skins_data)

        return processed_data
