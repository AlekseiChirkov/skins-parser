from dataclasses import dataclass

from core.settings import CSGO_MARKET_URL
from csgo_market.validators import URLValidator


@dataclass
class CSGOMarketURL(URLValidator):
    """Class saving url to process"""

    def __init__(
            self, page: str = None, price_range: str = None,
            stickers: str = None
    ) -> None:
        """
        Initialize data of url to parse
        :param page: string number of page
        :param price_range: string range of price from to (100;10000)
        :param stickers: string boolean value 0 or 1
        :return: None
        """

        self.url: str = self.create_url_with_filters(
            page, price_range, stickers
        )

    def create_url_with_filters(
            self, page: str, price_range: str, stickers: str
    ) -> str:
        """
        Method creates url with filters
        :param page: string number of page
        :param price_range: string range of price from to (100;10000)
        :param stickers: string boolean value 0 or 1
        :return: string with filtered url
        """

        page = self.validate_page(page)
        price = self.validate_price_range(price_range)
        stickers = self.validate_stickers(stickers)
        url_filters = f'/?s=pop&r=&q=&p={page}&rs={price}&h=&fst={stickers}'
        return CSGO_MARKET_URL + url_filters

