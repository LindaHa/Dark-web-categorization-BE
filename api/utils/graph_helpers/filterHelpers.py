from typing import List

from api.models import FilterOptions


def get_filter_fields_from_client(options: FilterOptions) -> List[str]:
    fields = []

    if options.content:
        fields.append('content')
    if options.url:
        fields.append('url')

    return fields
