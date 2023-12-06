import requests
import json
import re
from time import sleep
from requests import Response
from pyquery import PyQuery
from libs.utils.parser import HtmlParser
parser = Scrapper()
# parser.execute("https://www.archive.bps.go.id/subject/2/komunikasi.html#subjekViewTab3")
parser.execute("https://www.archive.bps.go.id/subject/7/energi.html#subjekViewTab3")

class Main:
    def __init__(self) -> None:
        self.__paerser = HtmlParser
        pass

    def get_url(self, main_url):
        response: Response = requests.get(url=main_url)
        html = PyQuery(response.text)
        
        pass

    def ex(self, main_url):
        urls = self.get_url(main_url=main_url)


if __name__ == '__main__':
    main = Main
    main.ex(main_url="https://www.archive.bps.go.id/")
