import time
import requests
import threading


class ParseException(Exception):
    pass


class Parser:
    
    def __init__(self,FILE,PAUSE,THREADS):
        self.PAUSE = PAUSE
        links = self.load_list_from_file(FILE)
        self.start(links,THREADS)

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
        
    def start(self,links,THREADS):
        links_chunks = self.chunklist(links,THREADS) 
        for links_block in links_chunks:
            thr = threading.Thread(target=self.get_link, args=([links_block]))
            thr.start()
            thr.join()
                
    def get_link(self,block):
        for link in block:
            try:
                url = 'https://sort.diginetica.net/search?st='+link
                #&apiKey=D1K76714Q4&strategy=vectors_extended,zero_queries_predictor&fullData=true&withCorrection=true&withFacets=true&treeFacets=true&regionId=global&useCategoryPrediction=true&size=20&offset=0&showUnavailable=true&unavailableMultiplier=0.2&preview=false&withSku=false&sort=DEFAULT'
                print(f'Thread #{threading.get_native_id()} : get {url}')
                response = requests.get(link, timeout=10)

                if response.status_code != 200:
                    raise ParseException

            except Exception as e:
                print(e)
                raise e

        return response.text
            
        print(f'wait {self.PAUSE} sec...')
        time.sleep(self.PAUSE)