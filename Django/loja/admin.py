from django.contrib import admin

from .models import Item, Carrinho, Carrinho_Item

admin.site.register(Carrinho)
admin.site.register(Item)
admin.site.register(Carrinho_Item)