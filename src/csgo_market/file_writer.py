import os

import xlwt
from bs4 import BeautifulSoup


class FileWriter:
    """Class to write data into a file"""

    @staticmethod
    def write_data_to_txt_file(
            data: BeautifulSoup, index: int, path: str
    ) -> str:
        """
        Method writes data into a txt file
        :param data: html page
        :param index: index of file to create
        :param path: folder path to create file in
        :return: str with created file path
        """

        pages_dir = os.listdir(path)
        if not pages_dir:
            with open(f'{path}/page_1.html', 'w') as file:
                file.write(str(data))
            return f'{path}/page_1.html'
        else:
            page = f'page_{index}.html'
            if page not in pages_dir:
                with open(f'{path}/{page}', 'w') as file:
                    file.write(str(data))
            return f'{path}/{page}'

    @classmethod
    def convert_skins_data_to_excel(cls, data: list) -> None:
        """
        Method converts list data to excel sheet
        :param data: list with data
        :return: None
        """

        print('Converting...')
        work_book = xlwt.Workbook()
        sheet = work_book.add_sheet('Skins prices')
        columns = (
            'Название (качество)', 'Цена', 'Цена автопокупки',
            'Разница цена/автопокупка', 'Рекомендованная цена', 'Ссылка',
            'Цена в стим', 'Ссылка', 'Кол-во', 'Разница цена/цена в стим',
        )
        for num, name in enumerate(columns):
            sheet.write(0, num, name)

        for i in range(len(data)):
            for j in range(len(data[i])):
                sheet.write(i+1, j, data[i][j])

        work_book.save("../excel_files/skins_prices.xls")
        print('Finished', work_book)
