<template>
  <v-app id="inspire">
    <v-app-bar
      app
      extended
    >

      <v-toolbar-title>Cavalo Variedades</v-toolbar-title>

      <v-spacer></v-spacer>
    </v-app-bar>

    <v-main>
      <v-container>
        <v-row>
          <v-col
            v-for="item in itens"
            :key="item.id"
            cols="4"
          >
            <v-card height="300" :title="item.nome_item">
              <img :src="item.foto.url" alt="" height="150">
              <p>Estoque: {{ item.quantidade }}</p>
              <v-btn>Adicionr ao carrinho</v-btn>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>


<script setup>

import LojaApi from '@/api/loja';
import { ref, onMounted } from "vue";

const lojaApi = new LojaApi();
const itens = ref([]);
const carrinho_itens = ref([])

const nome_item = ref('')
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

async function adicionarItemCarrinho(id) {
  await lojaApi.adicionarCarrinho({
    quantidade: 1,
    item: id,
  });
  carrinho_itens.value = await lojaApi.buscarCarrinho();
}

async function removerItem(id) {
  await lojaApi.removerItemCarrinho(id);
  carrinho_itens.value = await lojaApi.buscarCarrinho();
}
</script>
