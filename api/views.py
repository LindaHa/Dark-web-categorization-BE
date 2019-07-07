from rest_framework.response import Response
from rest_framework import viewsets, status

from api.models import Page
from api.utils.graph_helpers import Graph, find_strong_components
from . import serializers
from .repositories import ElasticSearchRepository

pages = [
    Page(id="0", url="0", title="0", links=[{"link": "2"}, {"link": "3"}], content="0"),
    Page(id="1", url="1", title="1", links=[{"link": "0"}], content="1"),
    Page(id="2", url="2", title="2", links=[{"link": "1"}], content="2"),
    Page(id="3", url="3", title="3", links=[], content="3"),
    Page(id="4", url="4", title="4", links=[], content="4"),
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
            # graph = Graph(response)
            # graph.find_strongly_connected_components()
            # result = graph.components
            # result = response
            result = find_strong_components(pages)

        if result is None:
            return Response({"result": False, "message": "Could not get response"})

        serializer = serializers.PageSerializer(
            instance=result, many=True)
        # return Response({"result": True, "data": serializer.data})
        return Response({"result": True, "data": result})
