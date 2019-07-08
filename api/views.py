from rest_framework.response import Response
from rest_framework import viewsets

from api.models import Page
from api.utils.graph_helpers import get_linked_components
from . import serializers
from .repositories import ElasticSearchRepository

pages = [
    Page(id="zero", url="zero", title="zero", links=[{"link": "two"}, {"link": "three"}], content="zero"),
    Page(id="one", url="one", title="one", links=[{"link": "zero"}], content="one"),
    Page(id="two", url="two", title="two", links=[{"link": "one"}], content="two"),
    Page(id="three", url="three", title="three", links=[{"link": "five"}], content="three"),
    Page(id="four", url="four", title="four", links=[], content="four"),
    Page(id="five", url="five", title="five", links=[{"link": "fohr"}], content="five"),
]


class PageViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = serializers.PageSerializer
    el_repository = ElasticSearchRepository()

    def list(self, request):
        if "url_filter" in request.query_params and request.query_params["url_filter"] != "":
            search_column = "content"
            search_phrase = request.query_params["url_filter"]
            result = self.el_repository.basic_search(search_column, search_phrase)
        else:
            response = self.el_repository.fetch_all()
            # result = response
            result = get_linked_components(response)

        if result is None:
            return Response({"result": False, "message": "Could not get response"})
        serializer = serializers.ComponentSerializer(
            instance=result, many=True)
        return Response({"result": True, "data": serializer.data})
        # return Response({"result": True, "data": result})
