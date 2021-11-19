import requests

CSGO_MARKET_PRICE = '200;5000'
CSGO_MARKET_URL = "https://market.csgo.com"
STEAM_MARKET_URL = "https://steamcommunity.com/market/search?q="
SESSION = requests.Session()
SESSION.headers.update(
    {
        'referer': 'https://market.csgo.com/',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux '
                      'x86_64; rv:93.0) Gecko/20100101 Firefox/93.0',
    }
)
