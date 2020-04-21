import shelve
from typing import Dict
from api.models import Page

page_shelf_name = 'backup_db_response'
page_shelf_key_prefix = 'pages_batch_'
page_shelf_batch_count = 'backed_up'
pages_no_content = 'pages_without_content'


def get_shelved_pages() -> Dict[str, Page]:
    shelf = shelve.open(page_shelf_name)
    pages = {}
    if page_shelf_batch_count in shelf:
        number_of_batches = shelf[page_shelf_batch_count]
        while number_of_batches > 0:
            print(number_of_batches)
            new_batch = shelf[page_shelf_key_prefix + str(number_of_batches - 1)]
            pages.update(new_batch)
            number_of_batches -= 1
    shelf.close()

    return pages
