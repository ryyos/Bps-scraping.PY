import math
import requests
import json
import re
from time import sleep
from requests import Response
from pyquery import PyQuery
from libs.utils.parser import HtmlParser

class Scrapper:
    def __init__(self) -> None:
        self.__parser = HtmlParser()
        self.__main_url = 'https://www.archive.bps.go.id'
        self.__results = dict()
        self.__results['data'] = []
        pass


    def filter_data(self, data) -> str:
        return data.replace(',', '.').replace('\u2009', '').replace(' ', '')
    
    

    def filter_url(self, url):
        __urls = []

        response = requests.get(url)
        html = PyQuery(response.text)
        for no, html in enumerate(html.find('#listTabel1 tr')):
            if(self.__parser.ex(html=html, selector='td:nth-child(2)').text() == ""): continue
            
            self.__results['data'].append({
                'id' : no,
                'title' : self.__parser.ex(html=html, selector='td:nth-child(2)').text(),
                'update' : self.__parser.ex(html=html, selector='td:nth-child(3)').text(),
                'keterangan' : self.__parser.ex(html=html, selector='td:nth-child(4)').text()
            })

            href_element = self.__parser.ex(html=html, selector='td:nth-child(2) a').attr('href')
            __urls.append(f'{self.__main_url}{href_element}' if self.__main_url not in str(href_element) else href_element)
            no +=1

        return __urls


    def create_url(self, urlReqs: str, newValue: int) -> str:

        pieces_url = urlReqs.split('/')
        
        index = pieces_url.index('indicator') + 3
        pieces_url[index] = str(newValue)

        return '/'.join(pieces_url)

    def extract_data(self, urlReqs: str):
        __urls_tables = dict()
        __temporary = []
        __urls_tables = []
        __url_val = 1

        while True:
            __url = self.create_url(urlReqs=urlReqs, newValue=__url_val)
            print(__url)
            response: Response = requests.get(url=__url)
            html: PyQuery = PyQuery(response.text)

            if not html.find('thead tr th:nth-child(2)'):
                break
            __url_val += 1
    
            __urls_tables.append(__url)
    
            tables = self.__parser.ex(html=html, selector='#tablex')
            if len(tables.find(selector='thead tr')) > 2:
                
                __headers = []
                for head in tables.find(selector='thead tr:first-child th'):
                    __headers.append(re.sub(r'\s+', ' ', head.text.strip()))

                __key_layer2 = []
                for head in tables.find(selector='thead tr:nth-child(2) th'):
                    __key_layer2.append(re.sub(r'\s+', ' ', head.text.strip()))

                __key_layer3 = []
                for head in tables.find(selector='thead tr:nth-child(3) th'):
                    __key_layer3.append(re.sub(r'\s+', ' ', head.text.strip()).replace('\u2009', ' '))
            
                for value in tables.find(selector='tbody tr'):
                    __data_table = {
                        __headers[0]: self.__parser.ex(html=value, selector='td:first-child').text(),
                        __headers[1]: {
                            layer2: {
                                __key_layer3[i]: self.filter_data(self.__parser.ex(html=value, selector=f'td:nth-child({i + 2 + int(len(__key_layer3) / len(__key_layer2)) * index_layer2})').text())
                                for i in range(int(len(__key_layer3) / len(__key_layer2)))

                            } for index_layer2, layer2 in enumerate(__key_layer2)
                        }
                    }
                
                    
                    existing_data = next((item for item in __temporary if item.get(__headers[0]) == __data_table[__headers[0]]), None)
                    if existing_data:
                        for layer2 in __key_layer2:
                            try:

                                if(existing_data[__headers[1]][layer2].keys() == __data_table[__headers[1]][layer2].keys()):
                                    __temporary.append(existing_data[__headers[1]][layer2].append(__data_table[__headers[1]][layer2]))
                                else:
                                    existing_data[__headers[1]][layer2].update(__data_table[__headers[1]][layer2])

                            except:
                                __temporary.append(__data_table)

                    else:
                        __temporary.append(__data_table)

            else:

                __headers = []
                for head in tables.find(selector = 'thead tr:first-child th'):
                    __headers.append(re.sub(r'\s+', ' ', head.text.strip()))


                __key_layer2 = []
                for layer2 in tables.find(selector = 'thead tr:last-child th'):
                    __key_layer2.append(re.sub(r'\s+', ' ', layer2.text.strip()).replace('\u2009', ' '))
                    

                for value in tables.find('tbody tr'):
                    __data_table = {
                        __headers[0]: self.__parser.ex(html=value, selector='td:first-child').text(),
                        __headers[1]: {
                            layer2: self.filter_data(self.__parser.ex(html=value, selector=f'td:nth-child({index_layer2 + 2})').text())
                            for index_layer2, layer2 in enumerate(__key_layer2)
                        }
                    }

                    existing_data = next((item for item in __temporary if item.get(__headers[0]) == __data_table[__headers[0]]), None)

                    if existing_data:
                        existing_data[__headers[1]].update(__data_table[__headers[1]])
                    else:
                        __temporary.append(__data_table)

        return[__urls_tables, __temporary]

                



    def ex(self, req_url):

        urls = self.filter_url(req_url)
        for index, url in enumerate(urls):
            print('Outer --> ' ,url)
            if 'indicator' not in url: continue
            results = self.extract_data(urlReqs=url)
            self.__results['data'][index].update({
                'url_tables': results[0],
                'data_tables': results[1]
            })

            
        return self.__results






