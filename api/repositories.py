from pip._vendor import requests
from api.utils.parsers import get_pages_from_json


class ElasticSearchRepository(object):
    def __init__(self, **kwargs):
        self.end_point_url = "http://147.251.124.23:9200/tor,i2p/"

    def basic_search(self, search_column, search_phrase):
        payload = {
            "query": {
                # "multi_match": {
                #     "query": search_phrase,
                #     "fields": search_column
                # },
                "bool": {
                    "must": [
                        {
                            "match": {search_column: search_phrase}
                        }
                    ]
                }
            }
        }
        response = requests.post(self.end_point_url + "_search", json=payload)
        if response.status_code == 200:
            json = response.json()
            pages = get_pages_from_json(json)
            return pages
        else:
            return None

    def fetch_all(self):
        payload = {
            "from": 0, "size": 1000,
            "query": {
                "match_all": {}
            }
        }
        response = requests.post(self.end_point_url + "_search", json=payload)
        if response.status_code == 200:
            json = response.json()
            pages = get_pages_from_json(json)
            return pages
        else:
            return None
