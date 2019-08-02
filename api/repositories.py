from pip._vendor import requests
from api.utils.parsers import get_pages_from_json, get_total_in_db, get_scroll_id, get_hits


CHUNK_SIZE = 500


class ElasticSearchRepository(object):
    def __init__(self, **kwargs):
        self.server = "http://147.251.124.23:9200/"
        self.end_point_url = self.server + "tor,i2p/"

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

    def fetch_chunk(self, scroll_id):
        payload = {
            "scroll": "1m",
            "scroll_id": scroll_id
        }
        response = requests.post(self.server + "_search/scroll", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def fetch_all(self):
        payload = {
            "size": CHUNK_SIZE,
            "query": {
                "match_all": {}
            }
        }

        response = requests.post(self.end_point_url + "_search?scroll=1m", json=payload)
        final_pages = {}
        if response.status_code == 200:
            json = response.json()
            scroll_id = get_scroll_id(json)
            final_pages = get_pages_from_json(json)
            hits = get_hits(json)
            i = 0

            while hits:
                chunk_json = self.fetch_chunk(scroll_id)

                scroll_id = get_scroll_id(chunk_json)
                hits = get_hits(chunk_json)
                pages = get_pages_from_json(chunk_json)

                if pages:
                    final_pages.update(pages)

                print(i)
                i += 1

        return final_pages
