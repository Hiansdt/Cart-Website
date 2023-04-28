from loja.models import Item, Carrinho_Item
from rest_framework.serializers import ModelSerializer

class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class Carrinho_ItemSerializer(ModelSerializer):
    class Meta:
        model = Carrinho_Item
        fields = '__all__'