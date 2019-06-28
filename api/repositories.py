`from pip._vendor import requests

class ElasticSearchRepository(object):
    def __init__(self, **kwargs):
        self.end_point_url = "http://147.251.124.23:9200/tor,i2p/"

    def basicSearch(self, search_column, search_phrase):
        r = requests.get(self.end_point_url + "_search?q=" + search_column + ":" + search_phrase)
        if r.status_code == 200:
            json = r.json()

        else:
            return None


