from typing import Dict

from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import viewsets
from api.models import Page, Link, DetailsOptions, FilterOptions
from api.utils.caching_helpers import get_cached_all_groups, cache_all_groups, cache_all_groups_by_category, \
    get_cached_all_groups_by_category
from api.utils.convertors import convert_groups_to_meta_groups
from api.utils.graph_helpers.graph_helpers import get_linked_groups
from api.utils.graph_helpers.group_by_helpers import divide_pages_by_category, GroupByMode
from api.utils.graph_helpers.level_helpers import get_subgroups_of_group, get_group
from api.utils.graph_helpers.details_helpers import get_group_details, get_pages_details, \
    get_single_page_details_not_from_db
from . import serializers
from .repositories import ElasticSearchRepository
from .utils.graph_helpers.filterHelpers import get_filter_fields_from_client


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


# Returns pages or community-members divided into communities or a specific page
class GroupsByLinkViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    el_repository = ElasticSearchRepository()

    def list(self, request):
        if are_params_present(["id"], request.query_params):
            group_id = request.query_params["id"]
            try:
                groups = get_subgroups_of_group(group_id, self.el_repository, GroupByMode.LINK.value)
            except NotFound:
                return handle_db_problem()

            result = convert_groups_to_meta_groups(groups)

        else:
            groups = get_cached_all_groups()
            if not groups:
                try:
                    response = self.el_repository.fetch_all()
                except NotFound:
                    return handle_db_problem()
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

    def create(self, request):
        if are_params_present(["options"], request.data) \
                and are_params_present(["url_filter"], request.query_params):
            options_data = request.data["options"]
            options = FilterOptions(
                url=options_data["url"],
                content=options_data["content"],
            )
            filter_fields = get_filter_fields_from_client(options)
            url = request.query_params["url_filter"]
            try:
                response = self.el_repository.basic_search(search_fields=filter_fields, search_phrase=url)
            except NotFound:
                return handle_db_problem()
            if not response:
                result = None
            else:
                groups = get_linked_groups(response)
                result = convert_groups_to_meta_groups(groups)

        else:
            result = None

        if result is None:
            return Response({"result": False, "message": "Could not get response"}, content_type='application/json')
        serializer = serializers.MetaGroupSerializer(
            instance=result, many=True)
        return Response(
            {"result": True, "data": serializer.data}
        )


# Returns groups divided by category or group members divided into communities
class GroupsByCategoryViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    el_repository = ElasticSearchRepository()

    def list(self, request):
        if are_params_present(["id"], request.query_params):
            group_id = request.query_params["id"]
            try:
                groups = get_subgroups_of_group(group_id, self.el_repository, GroupByMode.CATEGORY.value)
            except NotFound:
                return handle_db_problem()

            result = convert_groups_to_meta_groups(groups)

        else:
            groups = get_cached_all_groups_by_category()
            if not groups:
                try:
                    pages = self.el_repository.fetch_all()
                except NotFound:
                    return handle_db_problem()

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

    def create(self, request):
        if are_params_present(["options"], request.data) \
                and are_params_present(["url_filter"], request.query_params):
            options_data = request.data["options"]
            options = FilterOptions(
                url=options_data["url"],
                content=options_data["content"],
            )
            filter_details = get_filter_fields_from_client(options)
            url = request.query_params["url_filter"]
            try:
                response = self.el_repository.basic_search(search_fields=filter_details, search_phrase=url)
            except NotFound:
                return handle_db_problem()

            if not response:
                result = None
            else:
                groups = divide_pages_by_category(response)
                result = convert_groups_to_meta_groups(groups)
        else:
            result = None

        if result is None:
            return Response({"result": False, "message": "Could not get response"}, content_type='application/json')
        serializer = serializers.MetaGroupSerializer(
            instance=result, many=True)
        return Response(
            {"result": True, "data": serializer.data}
        )


# Returns group details based on detail options
class GroupDetailsViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    el_repository = ElasticSearchRepository()

    def create(self, request):
        if are_params_present(["id", "options"], request.data) \
                and are_params_present(["groupby"], request.query_params):
            options_data = request.data["options"]
            options = DetailsOptions(
                title=options_data["title"],
                category=options_data["category"],
                content=options_data["content"],
                links=options_data["links"],
            )
            group_id = request.data["id"]
            group_by_mode = request.query_params["groupby"]
            try:
                group = get_group(group_id, self.el_repository, group_by_mode)
            except NotFound:
                return handle_db_problem()

            result = get_group_details(group=group, options=options)
        else:
            result = None

        if result is None:
            return Response({"result": False, "message": "Could not get response"}, content_type='application/json')
        serializer = serializers.PageDetailsSerializer(
            instance=result, many=True)
        return Response(
            {"result": True, "data": serializer.data}
        )


# Returns page details based on detail options
class PageDetailsViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    el_repository = ElasticSearchRepository()

    def create(self, request):
        if are_params_present(["options", "id"], request.data):
            options_data = request.data["options"]
            options = DetailsOptions(
                title=options_data["title"],
                category=options_data["category"],
                content=options_data["content"],
                links=options_data["links"],
            )
            url = request.data["id"]
            try:
                pages = self.el_repository.basic_search(search_fields=["url"], search_phrase=url)
                pages = {url: pages[url]} if url in pages else pages
                result = get_pages_details(pages=pages, options=options, are_whole=True)[0]
            except NotFound:
                result = get_single_page_details_not_from_db(url=url, options=options)
        else:
            result = None

        if result is None:
            return handle_db_problem()
        serializer = serializers.PageDetailsSerializer(
            instance=result, many=False)
        return Response(
            {"result": True, "data": serializer.data}
        )


def handle_db_problem() -> Response:
    """
    :return: Returns a response with status code 503 with a message
    :rtype: Response
    """
    return Response(
        {"result": False, "message": "There seems to be a problem with the database."},
        status=503, content_type='application/json'
    )
