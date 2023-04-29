<template>
  <div>
    <div v-for="item of itens" :key="item.id">
      {{ item.nome_item }}
      <br/>
      {{ item.valor }}
      <br>
      {{ item.id }}
      <img alt="">
    </div>
    <div>
      add item
      <input type="text" placeholder="nome" v-model="nome_item">
      <input type="number" placeholder="quantidade" v-model="quantidade_item">
      <input type="number" placeholder="valor" v-model="valor_item">

      <button @click="adicionarItem">Enviar</button>
    </div>
  </div>
</template>

<script setup>

import LojaApi from '@/api/loja';
import { ref, onMounted } from "vue";

const lojaApi = new LojaApi();
const itens = ref([]);

const nome_item = ref('')
const id_item = ref('')
const quantidade_item = ref('')
const valor_item =  ref('')

onMounted(
  async function buscar() {
    itens.value = await lojaApi.buscarItens();
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
</script>
