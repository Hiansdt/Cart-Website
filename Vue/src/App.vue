<template>
  <div>
    <div v-for="item of itens" :key="item.id">
      {{ item.nome_item }}
      <br />
      {{ item.valor }}
      <br>
      {{ item.id }}
      <img alt="">
      <button @click="adicionarItemCarrinho(item)">Adicionar ao carrinho</button>
    </div>
    <div>
    </div>

    <div>
      carrinho
      <div v-for="item of carrinho_itens" :key="item.id">
        {{ itens[item.item] }}
      </div>
    </div>
  </div>
</template>

<script setup>

import LojaApi from '@/api/loja';
import { ref, onMounted } from "vue";

const lojaApi = new LojaApi();
const itens = ref([]);
const carrinho_itens = ref([])

const nome_item = ref('')
const id_item = ref('')
const quantidade_item = ref('')
const valor_item = ref('')
const response = ref('');

const quantidade_item_carrinho = ref('')

onMounted(
  async function buscar() {
    itens.value = await lojaApi.buscarItens();
    carrinho_itens.value = await lojaApi.buscarCarrinho();
  }
)

async function adicionarItem() {
  await lojaApi.enviarItem({
    nome_item: nome_item.value,
    quantidade: quantidade_item.value,
    valor: valor_item.value
  });
  itens.value = await lojaApi.buscarItens();
}

async function adicionarItemCarrinho(id) {
  await lojaApi.adicionarCarrinho({
    id: 1,
    quantidade: 1,
    item: id,
  });
  carrinho_itens.value = await lojaApi.buscarCarrinho();
}
</script>
