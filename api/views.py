from typing import Dict

from rest_framework.response import Response
from rest_framework import viewsets
from api.models import Page, Link, PageDetails
from api.utils.caching_helpers import get_cached_all_groups, cache_all_groups, cache_all_groups_by_category, \
    get_cached_all_groups_by_category
from api.utils.convertors import convert_groups_to_meta_groups
from api.utils.graph_helpers.graph_helpers import get_linked_groups
from api.utils.graph_helpers.group_by_helpers import divide_pages_by_category, GroupByMode
from api.utils.graph_helpers.level_helpers import get_subgroups_of_group, get_group
from api.utils.graph_helpers.details_helpers import get_group_details, get_page_details
from . import serializers
from .repositories import ElasticSearchRepository

mock_pages = {
    "zero.onion": Page(id="zero.onion", url="zero.onion", title="zero", links=[Link(link="two.onion"), Link(link="three.onion")], content="zero"),
    "one.onion": Page(id="one.onion", url="one.onion", title="one", links=[Link(link="zero.onion")], content="one"),
    "two.onion": Page(id="two.onion", url="two.onion", title="two", links=[Link(link="one.onion")], content="two"),
    "three.onion": Page(id="three.onion", url="three.onion", title="three", links=[Link(link="five.onion")], content="three"),
    "four.onion": Page(id="four.onion", url="four.onion", title="four", links=[], content="four"),
    "five.onion": Page(id="five.onion", url="five.onion", title="five", content="five"),
    'xordoquy.onion': Page(id='xordoquy.onion', content='Sleep some', url='xordoquy.onion', links=[Link(link='xordoquy.onion/guns'), Link(link='xordoquy.onion/drugs')]),
    'xordoquy.onion/guns': Page(id='xordoquy.onion/guns', content='Sleep more', url='xordoquy.onion/guns'),
    'xordoquy.onion/drugs': Page(id='xordoquy.onion/drugs', content='Sleep less', url='xordoquy.onion/drugs', links=[Link(link='xordoquy.onion/drugs'), Link(link='wow.onion/drugs'), Link(link='road.onion/drugs')]),
    'wow.onion': Page(id='wow.onion',content='Wow some', url='wow.onion', links=[Link(link='wow.onion/drugs'), Link(link='wow.onion/hacking'), Link(link='wow.onion/laundry')]),
    'wow.onion/drugs': Page(id='wow.onion/drugs', content='Wow better', url='wow.onion/drugs'),
    'wow.onion/hacking': Page(id='wow.onion/hacking',content='Wow less', url='wow.onion/hacking', links=[Link(link='for4.onion/hacking'), Link(link='for4.onion')]),
    'wow.onion/laundry': Page(id='wow.onion/laundry', content='Wow cleaner', url='wow.onion/laundry'),
    'bling.onion': Page(id='bling.onion', content='Bling some', url='bling.onion', links=[Link(link='bling.onion/guns')]),
    'bling.onion/guns': Page(id='bling.onion/guns', content='Bling more', url='bling.onion/guns'),
    'road.onion/': Page(id='road.onion/', content='Drive some', url='road.onion/', links=[Link(link='road.onion/guns'), Link(link='road.onion/porn'), Link(link='road.onion/drugs')]),
    'road.onion/guns': Page(id='road.onion/guns', content='Drive faster', url='road.onion/guns'),
    'road.onion/porn': Page(id='road.onion/porn', content='Drive less', url='road.onion/porn', links=[Link(link='xordoquy.onion')]),
    'road.onion/drugs': Page(id='road.onion/drugs', content='Drive better', url='road.onion/drugs', links=[Link(link='road.onion/')]),
    'for4.onion': Page(id='for4.onion', content='Code some', url='for4.onion', links=[Link(link='for4.onion/drugs'), Link(link='for4.onion/hacking')]),
    'for4.onion/drugs': Page(id='for4.onion/drugs', content='Code better', url='for4.onion/drugs'),
    'for4.onion/hacking': Page(id='for4.onion/hacking', content='Code faster', url='for4.onion/hacking', links=[Link(link='wow.onion/hacking')]),
    'blrn.onion': Page(id='blrn.onion', content='Do some', url='blrn.onion', links=[Link(link='blrn.onion/services')]),
    'blrn.onion/services': Page(id='blrn.onion/services', content='Do better', url='blrn.onion/services', links=[Link(link='for4.onion/hacking')]),
}


def are_params_present(my_params: [str], query_params: Dict[str, str]) -> bool:
    """
    :param my_params: the checked for parameters
    :type my_params: List[str]
    :param query_params: the given parameters
    :type query_params: Dict[str, str]
    :return: returns true if the parameters are all present, otherwise false
    :rtype: bool
    """
    if not query_params:
        return False

    for param in my_params:
        present = param in query_params and query_params[param]
        if not present:
            return False

    return True


class GroupsByLinkViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    el_repository = ElasticSearchRepository()

    def list(self, request):
        if are_params_present(["url_filter"], request.query_params):
            search_column = "content"
            search_phrase = request.query_params["url_filter"]

            response = self.el_repository.basic_search(search_column, search_phrase)
            groups = get_linked_groups(response)
            result = convert_groups_to_meta_groups(groups)

        elif are_params_present(["id"], request.query_params):
            group_id = request.query_params["id"]
            groups = get_subgroups_of_group(group_id, self.el_repository, GroupByMode.LINK.value)
            result = convert_groups_to_meta_groups(groups)

        else:
            groups = get_cached_all_groups()
            if not groups:
                response = self.el_repository.fetch_all()
                groups = get_linked_groups(response)
                cache_all_groups(groups)
            result = convert_groups_to_meta_groups(groups)

        if result is None:
            return Response({"result": False, "message": "Could not get response"}, content_type='application/json')
        serializer = serializers.MetaGroupSerializer(
            instance=result, many=True)
        return Response(
            {"result": True, "data": serializer.data}
        )


class GroupsByCategoryViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    el_repository = ElasticSearchRepository()

    def list(self, request):
        if are_params_present(["url_filter"], request.query_params):
            search_column = "content"
            search_phrase = request.query_params["url_filter"]

            response = self.el_repository.basic_search(search_column, search_phrase)
            groups = get_linked_groups(response)
            result = convert_groups_to_meta_groups(groups)

        elif are_params_present(["id"], request.query_params):
            group_id = request.query_params["id"]
            groups = get_subgroups_of_group(group_id, self.el_repository, GroupByMode.CATEGORY.value)
            result = convert_groups_to_meta_groups(groups)

        else:
            groups = get_cached_all_groups_by_category()

            if not groups:
                pages = self.el_repository.fetch_all()
                groups = divide_pages_by_category(pages)
                cache_all_groups_by_category(groups)

            result = convert_groups_to_meta_groups(groups)

        if result is None:
            return Response({"result": False, "message": "Could not get response"}, content_type='application/json')
        serializer = serializers.MetaGroupSerializer(
            instance=result, many=True)
        return Response(
            {"result": True, "data": serializer.data}
        )


class GroupDetailsViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    el_repository = ElasticSearchRepository()

    def create(self, request):
        if are_params_present(["id", "groupby"], request.query_params):
            group_id = request.query_params["id"]
            group_by_mode = request.query_params["groupby"]
            group = get_group(group_id, self.el_repository, group_by_mode)

            result = get_group_details(group)
        else:
            result = None

        if result is None:
            return Response({"result": False, "message": "Could not get response"}, content_type='application/json')
        serializer = serializers.GroupDetailsSerializer(
            instance=result, many=False)
        return Response(
            {"result": True, "data": serializer.data}
        )


class PageDetailsViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    el_repository = ElasticSearchRepository()

    def list(self, request):
        if are_params_present(["id"], request.query_params):
            page_id = request.query_params["id"]
            pages = self.el_repository.fetch_all()
            if not pages:
                result = None
            else:
                page = pages[page_id]
                result = get_page_details(page)
        else:
            result = None

        if result is None:
            return Response({"result": False, "message": "Could not get response"}, content_type='application/json')
        serializer = serializers.PageDetailsSerializer(
            instance=result, many=False)
        return Response(
            {"result": True, "data": serializer.data}
        )
