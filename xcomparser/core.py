import time
import json
import threading
from datetime import datetime
from queue import Queue
from threading import Thread
import requests
from bs4 import BeautifulSoup
import exceler as es


class ParseException(Exception):
    pass


class Parser:
    
    def __init__(self, file, pause, threads):
        self.pause = pause
        links = self.load_list_from_file(file)
        self.length = len(links)
        self.start(links, threads)

    @staticmethod
    def load_list_from_file(filename):
        ''' load links from file '''
        try:
            with open(filename) as file_name:
                links = file_name.readlines()
        except FileNotFoundError:
            raise '!!! Файл с артикулами не найден !!!'
        return [x.rstrip('\n') for x in links]

    @staticmethod
    def chunklist(links_in_list, size_of_chunk):
        ''' ГЕНЕРАТОР -- разбить список на список списков длинной size_of_chunk '''
        for i in range(0, len(links_in_list), size_of_chunk):
            yield links_in_list[i:i + size_of_chunk]

    def start(self, links, threads):
        self.que = Queue()
        results = []
        links_chunks = self.chunklist(links, threads)
        for links_block in links_chunks:
            threads_list = []
            for link in links_block:
                thr = Thread(target=lambda q, arg: q.put(
                    self.get_link(arg)), args=(self.que, link))
                thr.start()
                threads_list.append(thr)
            for thr in threads_list:
                thr.join()
            while not self.que.empty():
                results.append(self.que.get())
            # INFO AND SLEEP    
            self.length -= len(links_block)
            print(f'{datetime.now()}: {self.length} to finish...')
            print(f'wait {self.pause} sec...')
            time.sleep(self.pause)
        # DUMP OUT
        #print(results)
        es.ExcelService.create_table(results)

    @staticmethod
    def get_link(art):
        apikey = 'D1K76714Q4'
        try:
            url = 'https://sort.diginetica.net/search?st=' + art + '&fullData=true&apiKey=' + apikey
            print(f'Thread #{threading.get_native_id()} : get {url}')
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                raise ParseException
        except Exception as e:
            print(e)

        link = 'https://www.xcom-shop.ru' + json.loads(response.text)['products'][0]['link_url']
        img_link = json.loads(response.text)['products'][0]['image_url']
        brand = json.loads(response.text)['products'][0]['brand']

        try:
            if json.loads(response.text)['products'][0]['attributes']['код товара'][0]==art:
                art_found = True
            else:
                art_found = False
        except Exception as e:
            art_found = False
            print(f'ART: ошибка получения артикула (нет в поиске) {link}')
            
        try:
            response = requests.get(link, timeout=10)
            if response.status_code != 200:
                raise ParseException
        except Exception as e:
            print(e)

        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find(
            'h1', {'id': lambda x: x == 'card-main-title'}).getText().lstrip().rstrip()
            
        try:
            descr_long = soup.find(
                'p', {'class': lambda x: x == 'product-block-description__text'}).getText().strip()
        except:
            descr_long = '---'
            print(f'Нет полного описания для: {link}')

        descr_short = soup.find('div',
                                {'class': lambda x: x == 'product-block-description__last-block-wrap'}).contents[1].getText()
        descr = soup.find_all(
            'div', {'class': lambda x: x == 'product-block-description__block'})
        hars = descr[1].find_all(
            'li', {'class': lambda x: x == 'product-block-description__item'})
        descrdict = {}
        for _ in hars:
            second = False
            try:
                first = _.contents[1].getText().rstrip()
                second = _.contents[3].getText().lstrip().rstrip()
            except:
                pass
            finally:
                if second:
                    descrdict[first] = second
                    
        data = {'title': title, 'dlong': descr_long, 'dshort': descr_short,
                'hars': descrdict, 'img': img_link, 'brand': brand, 'art': art, 'art_found': art_found}
        return data
