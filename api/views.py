from rest_framework.response import Response
from rest_framework import viewsets, status

from . import serializers
from .models import Page


# Global variable used for the sake of simplicity.
# In real life, you'll be using your own interface to a data store
# of some sort, being caching, NoSQL, LDAP, external API or anything else

pages = {
    1: Page(id='9ed26dd9-738a-49f1-91a6-91ed5793fe5d', description='Sleep some', url='xordoquy.onion', categories='guns, drugs', linksTo='a07f0bc2-8bdb-4a0e-85f6-a037d71affe9, a077a831-6d9f-4d9c-ab1d-9ec3fb6abd31'),
    2: Page(id='a07f0bc2-8bdb-4a0e-85f6-a037d71affe9', description='Sleep more', url='xordoquy.onion/guns', categories='guns'),
    3: Page(id='a077a831-6d9f-4d9c-ab1d-9ec3fb6abd31', description='Sleep less', url='xordoquy.onion/drugs', categories='drugs', linksTo='f5e24f18-9878-4750-82ea-8026d0472baa, a077a831-6dsd-4d9c-ab1d-9ec3fb6abd31'),
    4: Page(id='b4889aed-c92f-4533-a5e0-0f6b600cd276', description='Wow some', url='wow.onion', categories='drugs, hacking, money laundry', linksTo='f5e24f18-9878-4750-82ea-8026d0472baa, 3f35e4ff-93fb-4796-9c11-385ada0392df, e12daf5d-ac6b-4acb-b789-725917f314d4'),
    5: Page(id='f5e24f18-9878-4750-82ea-8026d0472baa', description='Wow better', url='wow.onion/drugs', categories='drugs'),
    6: Page(id='3f35e4ff-93fb-4796-9c11-385ada0392df', description='Wow less', url='wow.onion/hacking', categories='hacking', linksTo='af35e4ff-93sb-4796-asf1-385ada0392df, 67589aed-c92f-df33-a5e0-0f6b600cd276'),
    7: Page(id='e12daf5d-ac6b-4acb-b789-725917f314d4', description='Wow cleaner', url='wow.onion/laundry', categories='money laundry'),
    8: Page(id='9ed26dd9-738a-49f1-91a6-91ed5793fe5d', description='Bling some', url='bling.onion', categories='guns', linksTo='a6df0bc2-8bdb-4a0e-85f6-a037d71affe9'),
    9: Page(id='a6df0bc2-8bdb-4a0e-85f6-a037d71affe9', description='Bling more', url='bling.onion/guns', categories='guns'),
    10: Page(id='abef0bc2-8bdb-4a0e-85f6-a037d71affe9', description='Drive some', url='road.onion/', categories='guns, porn, drugs', linksTo='a079dbc2-8bdb-4a0e-85f6-a03ets1afer9, a07f0as2-8sfb-4a0e-85f6-a037d71a4dd9, a077a831-6dsd-4d9c-ab1d-9ec3fb6abd31'),
    11: Page(id='a079dbc2-8bdb-4a0e-85f6-a03ets1afer9', description='Drive faster', url='road.onion/guns', categories='guns'),
    12: Page(id='a07f0as2-8sfb-4a0e-85f6-a037d71a4dd9', description='Drive less', url='road.onion/porn', categories='guns', linksTo='9ed26dd9-738a-49f1-91a6-91ed5793fe5d'),
    13: Page(id='a077a831-6dsd-4d9c-ab1d-9ec3fb6abd31', description='Drive better', url='road.onion/drugs', categories='drugs'),
    14: Page(id='67589aed-c92f-df33-a5e0-0f6b600cd276', description='Code some', url='for4.onion', categories='drugs, hacking', linksTo='gbc24f18-df78-47sa-82ea-8026d047a344, af35e4ff-93sb-4796-asf1-385ada0392df'),
    15: Page(id='gbc24f18-df78-47sa-82ea-8026d047a344', description='Code better', url='for4.onion/drugs', categories='drugs'),
    16: Page(id='af35e4ff-93sb-4796-asf1-385ada0392df', description='Code faster', url='for4.onion/hacking', categories='hacking', linksTo='3f35e4ff-93fb-4796-9c11-385ada0392df'),
    17: Page(id='e12daf5d-ac6b-4acb-b789-s45d43f314d4', description='Do some', url='blrn.onion', categories='services', linksTo='af340a1c-ce9a-4c58-b82c-8d5435ds4daf'),
    18: Page(id='af340a1c-ce9a-4c58-b82c-8d5435ds4daf', description='Do better', url='blrn.onion/services', categories='services', linksTo='af35e4ff-93sb-4796-asf1-385ada0392df'),
}


def get_next_page_id():
    return max(pages) + 1


class PageViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = serializers.PageSerializer

    def list(self, request):
        serializer = serializers.PageSerializer(
            instance=pages.values(), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = serializers.PageSerializer(data=request.data)
        if serializer.is_valid():
            page = serializer.save()
            page.id = get_next_page_id()
            pages[page.id] = page
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            page = pages[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.PageSerializer(instance=page)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            page = pages[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.PageSerializer(
            data=request.data, instance=page)
        if serializer.is_valid():
            page = serializer.save()
            pages[page.id] = page
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            page = pages[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.PageSerializer(
            data=request.data,
            instance=page,
            partial=True)
        if serializer.is_valid():
            page = serializer.save()
            pages[page.id] = page
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            page = pages[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        del pages[page.id]
        return Response(status=status.HTTP_204_NO_CONTENT)