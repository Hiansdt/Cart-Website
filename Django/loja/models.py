from django.db import models

class Item(models.Model):
    nome = models.CharField(max_length=255)
    quantidade = models.IntegerField(default=0)
    valor = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def __str__(self):
        return f'{self.nome} - {self.quantidade} - R${self.valor}'

class Carrinho(models.Model):
    itens = models.ManyToManyField(Item, related_name="carrinhos")

    def __str__(self):
        return "Carrinho"

class Carrinho_Item(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "Carrinho_Itens"

    def __str__(self):
        return f"{self.item.nome} - {self.quantidade}"
