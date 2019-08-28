from rest_framework.response import Response
from rest_framework import viewsets
from api.models import Page, Link
from api.utils.caching_helpers import get_cached_all_groups, cache_all_groups
from api.utils.convertors import convert_groups_to_meta_groups
from api.utils.graph_helpers.graph_helpers import get_linked_groups
from api.utils.graph_helpers.level_helpers import get_subgroups_of_group
from . import serializers
from .repositories import ElasticSearchRepository

pages = {
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


class PageViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = serializers.PageSerializer
    el_repository = ElasticSearchRepository()

    def list(self, request):
        is_lowest_level = False

        if "url_filter" in request.query_params and request.query_params["url_filter"] != "":
            search_column = "content"
            search_phrase = request.query_params["url_filter"]

            response = self.el_repository.basic_search(search_column, search_phrase)
            groups = get_linked_groups(response)
            result = convert_groups_to_meta_groups(groups)

        elif request.query_params and request.query_params["id"]:
            group_id = request.query_params["id"]
            groups = get_subgroups_of_group(group_id, self.el_repository)
            result = convert_groups_to_meta_groups(groups)

        else:
            groups_with_isolates_group = get_cached_all_groups()
            if groups_with_isolates_group:
                result = groups_with_isolates_group
            else:
                response = self.el_repository.fetch_all()
                groups = get_linked_groups(response)
                cache_all_groups(groups)
                result = convert_groups_to_meta_groups(groups)

        if result is None:
            return Response({"result": False, "message": "Could not get response"}, content_type='application/json')
        serializer = serializers.MetaGroupSerializer(
            instance=result, many=True)
        # serializer = serializers.PageSerializer(
        #     instance=pages.values(), many=True)
        return Response({"result": True, "data": serializer.data, "lowestLevel": is_lowest_level})
        # return Response({"result": True, "data": result})
