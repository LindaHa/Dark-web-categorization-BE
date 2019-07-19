from rest_framework.response import Response
from rest_framework import viewsets

from api.models import Page, Link
from api.utils.graph_helpers import get_linked_components
from . import serializers
from .repositories import ElasticSearchRepository

pages = {
    "zero.onion": Page(id="zero", url="zero.onion", title="zero", links=[Link(link="two.onion"), Link(link="three.onion")], content="zero"),
    "one.onion": Page(id="one", url="one.onion", title="one", links=[Link(link="zero.onion")], content="one"),
    "two.onion": Page(id="two", url="two.onion", title="two", links=[Link(link="one.onion")], content="two"),
    "three.onion": Page(id="three", url="three.onion", title="three", links=[Link(link="five.onion")], content="three"),
    "four.onion": Page(id="four", url="four.onion", title="four", links=[], content="four"),
    "five.onion": Page(id="five", url="five.onion", title="five", links=[Link(link="fohr.onion")], content="five"),
    'xordoquy.onion': Page(id='9ed26dd9-738a-49f1-91a6-91ed5793fe5d',content='Sleep some', url='xordoquy.onion', links=[Link(link='xordoquy.onion/guns'), Link(link='xordoquy.onion/drugs')]),
    'xordoquy.onion/guns': Page(id='a07f0bc2-8bdb-4a0e-85f6-a037d71affe9', content='Sleep more', url='xordoquy.onion/guns'),
    'xordoquy.onion/drugs': Page(id='a077a831-6d9f-4d9c-ab1d-9ec3fb6abd31',content='Sleep less', url='xordoquy.onion/drugs', links=[Link(link='wow.onion/drugs'), Link(link='road.onion/drugs')]),
    'wow.onion': Page(id='b4889aed-c92f-4533-a5e0-0f6b600cd276',content='Wow some', url='wow.onion', links=[Link(link='wow.onion/drugs'), Link(link='wow.onion/hacking'), Link(link='wow.onion/laundry')]),
    'wow.onion/drugs': Page(id='f5e24f18-9878-4750-82ea-8026d0472baa', content='Wow better', url='wow.onion/drugs'),
    'wow.onion/hacking': Page(id='3f35e4ff-93fb-4796-9c11-385ada0392df',content='Wow less', url='wow.onion/hacking', links=[Link(link='for4.onion/hacking'), Link(link='for4.onion')]),
    'wow.onion/laundry': Page(id='e12daf5d-ac6b-4acb-b789-725917f314d4', content='Wow cleaner', url='wow.onion/laundry'),
    'bling.onion': Page(id='9ed26dd9-738a-49f1-91a6-91ed5793fe5d', content='Bling some', url='bling.onion', links=[Link(link='bling.onion/guns')]),
    'bling.onion/guns': Page(id='a6df0bc2-8bdb-4a0e-85f6-a037d71affe9', content='Bling more', url='bling.onion/guns'),
    'road.onion/': Page(id='abef0bc2-8bdb-4a0e-85f6-a037d71affe9',content='Drive some', url='road.onion/', links=[Link(link='road.onion/guns'), Link(link='road.onion/porn'), Link(link='road.onion/drugs')]),
    'road.onion/guns': Page(id='a079dbc2-8bdb-4a0e-85f6-a03ets1afer9', content='Drive faster', url='road.onion/guns'),
    'road.onion/porn': Page(id='a07f0as2-8sfb-4a0e-85f6-a037d71a4dd9', content='Drive less', url='road.onion/porn', links=[Link(link='xordoquy.onion')]),
    'road.onion/drugs': Page(id='a077a831-6dsd-4d9c-ab1d-9ec3fb6abd31', content='Drive better', url='road.onion/drugs', links=[Link(link='road.onion/')]),
    'for4.onion': Page(id='67589aed-c92f-df33-a5e0-0f6b600cd276',content='Code some', url='for4.onion', links=[Link(link='for4.onion/drugs'), Link(link='for4.onion/hacking')]),
    'for4.onion/drugs': Page(id='gbc24f18-df78-47sa-82ea-8026d047a344', content='Code better', url='for4.onion/drugs'),
    'for4.onion/hacking': Page(id='af35e4ff-93sb-4796-asf1-385ada0392df', content='Code faster', url='for4.onion/hacking', links=[Link(link='wow.onion/hacking')]),
    'blrn.onion': Page(id='e12daf5d-ac6b-4acb-b789-s45d43f314d4', content='Do some', url='blrn.onion', links=[Link(link='blrn.onion/services')]),
    'blrn.onion/services': Page(id='af340a1c-ce9a-4c58-b82c-8d5435ds4daf', content='Do better', url='blrn.onion/services', links=[Link(link='for4.onion/hacking')]),
}


class PageViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = serializers.PageSerializer
    el_repository = ElasticSearchRepository()

    def list(self, request):
        if "url_filter" in request.query_params and request.query_params["url_filter"] != "":
            search_column = "content"
            search_phrase = request.query_params["url_filter"]
            response = self.el_repository.basic_search(search_column, search_phrase)
        else:
            response = self.el_repository.fetch_all()

        result = get_linked_components(pages)
        if result is None:
            return Response({"result": False, "message": "Could not get response"}, content_type='application/json')
        serializer = serializers.ComponentSerializer(
            instance=result, many=True)
        return Response({"result": True, "data": serializer.data}, content_type='application/json')
        # return Response({"result": True, "data": result})
