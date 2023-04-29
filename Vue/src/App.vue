<template>
  <div>
    <div v-for="item of itens" :key="item.id">
      {{ item.nome }}
      <br/>
      {{ item.valor }}
    </div>
  </div>
</template>

<script setup>

import ItensApi from '@/api/itens';
import { ref, onMounted } from "vue";

const itensApi = new ItensApi();
const itens = ref([]);

onMounted(
  async function buscar() {
    itens.value = await itensApi.buscarItens();
  }
)
</script>
