from django.shortcuts import render
from loja.models import Carrinho_Item, Item
from rest_framework.viewsets import ModelViewSet
from loja.serializers import ItemSerializer, Carrinho_ItemSerializer

class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    depth = 1

class Carrinho_itemViewSet(ModelViewSet):
    queryset = Carrinho_Item.objects.all()
    serializer_class = Carrinho_ItemSerializer