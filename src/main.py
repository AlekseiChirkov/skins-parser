from datetime import datetime

from file_decorators.decorators import clean_directory
from csgo_market.file_writer import FileWriter
from csgo_market.parsers import CSGOMarketFilteredPagesParser, SkinsParser
from steam_market.parsers import SteamParser


@clean_directory(['../pages/', '../skins_pages/', '../excel_files/'])
def main():
    """Function processing scripts"""

    price_range = input("Enter price range from to (100;900): ")
    stickers = input("Enter 0 or 1 to check sticker existence: ")

    start = datetime.now()

    parser = CSGOMarketFilteredPagesParser()
    parser.get_all_pages_to_process(price_range, stickers)
    market = SkinsParser().get_skins_data()
    steam = SteamParser()

    data_to_excel = []
    for item in market:
        skin_data = steam.get_skin_data(item[0])
        difference = item[1] - skin_data[0]

        for data in skin_data:
            item.append(data)

        item.append(difference)
        data_to_excel.append(item)

    writer = FileWriter()
    writer.convert_skins_data_to_excel(data_to_excel)

    end = datetime.now()
    print("Time passed:", end - start)


if __name__ == '__main__':
    main()
