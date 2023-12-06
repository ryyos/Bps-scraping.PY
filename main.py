import requests
import json
import os
from time import sleep
from requests import Response
from pyquery import PyQuery
from libs import HtmlParser
from libs import Scrapper
# parser = Scrapper()
# parser.execute("https://www.archive.bps.go.id/subject/2/komunikasi.html#subjekViewTab3")
# parser.execute("https://www.archive.bps.go.id/subject/7/energi.html#subjekViewTab3")

class Main:
    def __init__(self) -> None:
        self.__scrapper = Scrapper()
        self.__paerser = HtmlParser()
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

            # os.mkdir(f'data/{type.upper()}')

            for p in sideBar.find(f'#{type} p'):

                side = self.__paerser.ex(html=p, selector='a').attr('href')
                if side == None: break
                self.__get_name(side).upper()

            self.__scrapper.ex(req_url=self.__filter_url(url=side))

        

        pass

    def ex(self, main_url):
        urls = self.main(main_url=main_url)


if (__name__ == '__main__'):
    main = Main()
    main.ex(main_url="https://www.archive.bps.go.id/")
