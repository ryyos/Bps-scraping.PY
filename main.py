import requests
import json
import os
from time import sleep
from requests import Response
from pyquery import PyQuery
from libs import HtmlParser
from libs import Scrapper
from libs import Logs
from datetime import datetime as time
# parser = Scrapper()
# parser.execute("https://www.archive.bps.go.id/subject/2/komunikasi.html#subjekViewTab3")
# parser.execute("https://www.archive.bps.go.id/subject/7/energi.html#subjekViewTab3")

class Main:
    def __init__(self) -> None:
        self.__scrapper = Scrapper()
        self.__paerser = HtmlParser()
        self.__logs = Logs()
        self.__types = ['sosial', 'ekonomi', 'pertanian']
        self.__main_url = 'https://www.archive.bps.go.id'
        pass

    def __filter_url(self, url) -> str:
        url = url.replace('#subjekViewTab3', '')
        if self.__main_url not in url:
            return f'{self.__main_url}{url}'
        else:
            return url

    def __get_name(self, raw) -> str:
        __pieces_url = raw.split('.')
        __result = __pieces_url[0].split('/')
        return __result[-1]


    def main(self, main_url):

        response: Response = requests.get(url=main_url)
        html = PyQuery(response.text)
        sideBar = html.find(selector='#accordion-daftar-subjek2')

        for type in self.__types:

            os.mkdir(f'data/{type.upper()}')

            for p in sideBar.find(f'#{type} p'):

                side = self.__paerser.ex(html=p, selector='a').attr('href')
                if side == None: break

                __name_file = self.__get_name(side)
                __url_scrap = self.__filter_url(url=side)

                
                __result = {
                    'Type': type.upper(),
                    'times': time.now(),
                    'datas': self.__scrapper.ex(req_url=__url_scrap, type=type, title=__name_file)
                }
                

                with open(f'{type.upper()}/{__name_file.upper()}', 'w') as file:
                    json.dump(__result, file, indent=2)


    def ex(self, main_url):
        urls = self.main(main_url=main_url)


if (__name__ == '__main__'):
    main = Main()
    main.ex(main_url="https://www.archive.bps.go.id/")
