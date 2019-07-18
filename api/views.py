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

        result = get_linked_components(response)
        if result is None:
            return Response({"result": False, "message": "Could not get response"})
        serializer = serializers.ComponentSerializer(
            instance=result, many=True)
        return Response({"result": True, "data": serializer.data})
        # return Response({"result": True, "data": result})
