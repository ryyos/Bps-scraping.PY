import math
import requests
import json
import re
from time import sleep
from requests import Response
from pyquery import PyQuery
from libs.utils.parser import HtmlParser
from libs.utils.logs import Logs


class Scrapper:
    def __init__(self) -> None:
        self.__parser = HtmlParser()
        self.__logs = Logs()
        self.__main_url = 'https://www.archive.bps.go.id'
        self.__results = dict()
        self.__results['data'] = []
        self.urls = []
        pass


    def filter_data(self, data: str) -> any:
        data = data.replace(',', '.').replace('\u2009', '').replace(' ', '')
        try:
            return float(data)
        except:
            return data
    
    

    def filter_url(self, url: str) -> list:
        

        response: Response = requests.get(url)
        html: PyQuery = PyQuery(response.text)
        for no, html in enumerate(html.find('#listTabel1 tr')):
            if(self.__parser.ex(html=html, selector='td:nth-child(2)').text() == ""): continue
            href_element = self.__parser.ex(html=html, selector='td:nth-child(2) a').attr('href')
            if 'indicator' not in href_element: continue
            
            self.__results['data'].append({
                'id' : no,
                'title' : self.__parser.ex(html=html, selector='td:nth-child(2)').text(),
                'update' : self.__parser.ex(html=html, selector='td:nth-child(3)').text(),
                'keterangan' : self.__parser.ex(html=html, selector='td:nth-child(4)').text()
            })

            self.urls.append(f'{self.__main_url}{href_element}' if self.__main_url not in str(href_element) else href_element)
            no +=1
        return self.urls


    def create_url(self, urlReqs: str, newValue: int) -> str:

        pieces_url: list[str] = urlReqs.split('/')
        
        index: int = pieces_url.index('indicator') + 3
        pieces_url[index] = str(newValue)

        return '/'.join(pieces_url)

    def extract_data(self, urlReqs: str, log_type: str, log_title: str, log_base_url: str) -> list:
        urls_tables = dict()
        temporary: list[dict] = []
        urls_tables: list[str] = []
        url_val: int = 1

        while True:
            url: str = self.create_url(urlReqs=urlReqs, newValue=url_val)
            
            self.__logs.ex(type=log_type,title= log_title, base_url=log_base_url, child_url=url)

            response: Response = requests.get(url=url)
            html: PyQuery = PyQuery(response.text)

            if not html.find('thead tr th:nth-child(2)'):
                break
            url_val += 1
    
            urls_tables.append(url)
    
            tables = self.__parser.ex(html=html, selector='#tablex')
            if len(tables.find(selector='thead tr')) > 2:
                
                headers = [re.sub(r'\s', ' ', head.text.strip()) for head in tables.find(selector='thead tr:first-child th')]
                key_layer2 = [re.sub(r'\s+', ' ', head.text.strip()) for head in tables.find(selector='thead tr:nth-child(2) th')]
                key_layer3 = [re .sub(r'\s', ' ', head.text.strip()).replace('\u2009', ' ') for head in tables.find(selector='thead tr:nth-child(3) th')]
            
                for value in tables.find(selector='tbody tr'):
                    data_table = {
                        headers[0]: self.__parser.ex(html=value, selector='td:first-child').text(),
                        headers[1]: {
                            layer2: {
                                key_layer3[i]: self.filter_data(self.__parser.ex(html=value, selector=f'td:nth-child({i + 2 + int(len(key_layer3) / len(key_layer2)) * index_layer2})').text())
                                for i in range(int(len(key_layer3) / len(key_layer2)))

                            } for index_layer2, layer2 in enumerate(key_layer2)
                        }
                    }
                
                    
                    existing_data = next((item for item in temporary if item.get(headers[0]) == data_table[headers[0]]), None)
                    if existing_data:
                        for layer2 in key_layer2:
                            try:

                                if(existing_data[headers[1]][layer2].keys() == data_table[headers[1]][layer2].keys()):
                                    temporary.append(existing_data[headers[1]][layer2].append(data_table[headers[1]][layer2]))
                                else:
                                    existing_data[headers[1]][layer2].update(data_table[headers[1]][layer2])

                            except:
                                temporary.append(data_table)

                    else:
                        temporary.append(data_table)

            else:

                """
                    headers = []
                    for head in tables.find(selector = 'thead tr:first-child th'):  
                        headers.append(re.sub(r'\s+', ' ', head.text.strip()))
                """

                headers: list[str] = [re.sub(r'\s', ' ', head.text.strip()) for head in tables.find(selector='thead tr:first-child th')]
                key_layer2: list[str] = [re.sub(r'\s+', ' ', head.text.strip()) for head in tables.find(selector='thead tr:last-child th')]

                for value in tables.find('tbody tr'):
                    data_table = {
                        headers[0]: self.__parser.ex(html=value, selector='td:first-child').text(),
                        headers[1]: {
                            layer2: self.filter_data(self.__parser.ex(html=value, selector=f'td:nth-child({index_layer2 + 2})').text())
                            for index_layer2, layer2 in enumerate(key_layer2)
                        }
                    }

                    existing_data = next((item for item in temporary if item.get(headers[0]) == data_table[headers[0]]), None)

                    if existing_data:
                        existing_data[headers[1]].update(data_table[headers[1]])
                    else:
                        temporary.append(data_table)

        return[urls_tables, temporary]

                



    def ex(self, req_url, type, title) -> dict:

        urls: list[str] = self.filter_url(req_url)
        for index, url in enumerate(urls):

            
            try:
                results = self.extract_data(urlReqs=url, log_type=type, log_base_url=url, log_title=title)
            except:
                print('Request timeout!!')

            self.__results['data'][index].update({
                'url_tables': results[0],
                'data_tables': results[1]
            })

            
        return self.__results






