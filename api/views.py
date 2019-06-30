from rest_framework.response import Response
from rest_framework import viewsets, status

from . import serializers
from .repositories import ElasticSearchRepository


class PageViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = serializers.PageSerializer
    el_repository = ElasticSearchRepository()

    def list(self, request):
        if "url_filter" in request.query_params and request.query_params["url_filter"] != "":
            # pages_to_return = dict((k, v) for k, v in pages_to_return.items()
            # if request.query_params["url_filter"] in v.url)
            search_column = "content"
            search_phrase = request.query_params["url_filter"]
            result = self.el_repository.basic_search(search_column, search_phrase)
        else:
            result = self.el_repository.fetch_all()

        if result is None:
            return Response({"result": False, "message": "Could not get response"})

        serializer = serializers.PageSerializer(
            instance=result, many=True)
        return Response({"result": True, "data": serializer.data})

    # def create(self, request):
    #     serializer = serializers.PageSerializer(data=request.data)
    #     if serializer.is_valid():
    #         page = serializer.save()
    #         page.id = get_next_page_id()
    #         pages[page.id] = page
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def retrieve(self, request, pk=None):
    #     try:
    #         page = pages[int(pk)]
    #     except KeyError:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     except ValueError:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     serializer = serializers.PageSerializer(instance=page)
    #     return Response(serializer.data)
    #
    # def update(self, request, pk=None):
    #     try:
    #         page = pages[int(pk)]
    #     except KeyError:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     except ValueError:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     serializer = serializers.PageSerializer(
    #         data=request.data, instance=page)
    #     if serializer.is_valid():
    #         page = serializer.save()
    #         pages[page.id] = page
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def partial_update(self, request, pk=None):
    #     try:
    #         page = pages[int(pk)]
    #     except KeyError:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     except ValueError:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     serializer = serializers.PageSerializer(
    #         data=request.data,
    #         instance=page,
    #         partial=True)
    #     if serializer.is_valid():
    #         page = serializer.save()
    #         pages[page.id] = page
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def destroy(self, request, pk=None):
    #     try:
    #         page = pages[int(pk)]
    #     except KeyError:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     except ValueError:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     del pages[page.id]
    #     return Response(status=status.HTTP_204_NO_CONTENT)
