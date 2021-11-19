from bs4 import BeautifulSoup


class URLValidator:
    """Class to validate parser's url"""

    @staticmethod
    def validate_page(page: str) -> str:
        """
        Method validates page value
        :param page: string with page number
        :return: string of validated page number
        """

        return '0' if not page else page

    @staticmethod
    def validate_price_range(price_range: str) -> str:
        """
        Method validates price range
        :param price_range: string with price range
        :return: string of validated price range
        """

        return '0' if not price_range else price_range

    @staticmethod
    def validate_stickers(stickers: str) -> str:
        """
        Method validate stickers
        :param stickers: string with bool value 0 or 1
        :return: string of validated sticker value
        """

        return '0' if not stickers else stickers


class ParsedDataValidator:
    """Class to validate parsed data fields"""

    @staticmethod
    def validate_skin_name(page: BeautifulSoup) -> str:
        """
        Method validates skin name
        :param page: BeautifulSoup page
        :return: string skin name
        """

        try:
            name = page.find('div', class_='item-h1').find('h1').text
        except AttributeError:
            name = "No skin name"

        return name

    @staticmethod
    def validate_skin_quality(page: BeautifulSoup) -> str:
        """
        Method validates skin quality
        :param page: BeautifulSoup page
        :return: string skin quality
        """

        try:
            quality = page.find(
                'div', class_='item-appearance'
            ).find('span').text
        except AttributeError:
            quality = "No skin quality"

        return quality

    @staticmethod
    def validate_current_skin_price(page: BeautifulSoup) -> str:
        """
        Method validates current skin price
        :param page: BeautifulSoup page
        :return: string current skin price
        """

        try:
            price = page.find(
                'div', class_='ip-bestprice'
            )
            if price:
                price = str(price.text.strip().replace(' ', ''))
            else:
                price = 0
        except AttributeError:
            price = '0'

        return price

    @staticmethod
    def validate_auto_buy_skin_price(page: BeautifulSoup) -> str:
        """
        Method validates auto buy skin price
        :param page: BeautifulSoup page
        :return: string auto buy skin price
        """

        try:
            blocks = page.find_all('div', class_='rectanglestats')
            if len(blocks) > 1:
                stat_block = page.find_all('div', class_='rectanglestat')[5]
                b = stat_block.find('b')
                auto_buy_price = b.text.strip().replace(' ', '')
            else:
                stat_block = page.find_all('div', class_='rectanglestat')[1]
                b = stat_block.find('b')
                auto_buy_price = b.text.strip().replace(' ', '')
        except (AttributeError, IndexError):
            auto_buy_price = '0'

        return auto_buy_price

