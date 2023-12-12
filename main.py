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

class Main:
    def __init__(self) -> None:
        self.__paerser = HtmlParser()
        self.__logs = Logs()
        self.__types = ['sosial', 'ekonomi', 'pertanian']
        self.__main_url = 'https://www.archive.bps.go.id'

    def __filter_url(self, url) -> str:
        if self.__main_url not in url:
            return f'{self.__main_url}{url}'
        else:
            return url

    def __get_name(self, raw) -> str:
        __pieces_url = raw.split('.')
        __result = __pieces_url[0].split('/')
        return __result[-1]


    def main(self, main_url) -> None:

        response: Response = requests.get(url=main_url)
        html = PyQuery(response.text)
        sideBar = html.find(selector='#accordion-daftar-subjek2')

        for type in self.__types:

            # os.mkdir(f'data/{type.upper()}')
            print(type)
            for p in sideBar.find(f'#{type} p'):
                __scrapper = Scrapper()

                side = self.__paerser.ex(html=p, selector='a').attr('href')
                if side == None: break

                name_file = self.__get_name(side)
                url_scrap = self.__filter_url(url=side)
                print(url_scrap)


                __result = {
                    'Type': type.upper(),
                    'times': str(time.now()),
                    'datas': __scrapper.ex(req_url=url_scrap, type=type, title=name_file)
                }
                

                # with open(f'data/{type.upper()}/{name_file.upper()}.json', 'w') as file:
                #     json.dump(__result, file, indent=2)


    def ex(self, main_url) -> None:
        self.main(main_url=main_url)


if (__name__ == '__main__'):
    main = Main()
    main.ex(main_url="https://www.archive.bps.go.id/")
