<template>
  <v-app id="inspire">

    <v-navigation-drawer v-model="drawer" class="drawer" right>
      <h2>Carrinho</h2>
      <v-card v-for="item in carrinho_itens" :key="item.id" class="item_carrinho">
        {{ item.item.nome_item }}
        ({{ item.quantidade }})
        <v-icon @click="removerItem(item.id)" class="excluir">mdi-delete</v-icon>
        <v-icon @click="editarItem(item, item.quantidade += 1)"> mdi-plus </v-icon>
        <v-icon @click="editarItem(item, item.quantidade -= 1)"> mdi-minus </v-icon>
      </v-card>
    </v-navigation-drawer>

    <v-app-bar app extended>

      <v-btn icon>

        <v-icon @click="drawer = !drawer">
          mdi-cart
        </v-icon>

      </v-btn>

      <v-toolbar-title>Cavalo Variedades</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container>
        <v-row>
          <v-col v-for="item in itens" :key="item.id" cols="4">
            <v-card height="300" :title="item.nome_item">
              <img :src="item.foto.url" alt="" height="150">
              <p>Estoque: {{ item.quantidade }}</p>
              <v-btn @click="adicionarItemCarrinho(item)">Adicionar ao carrinho</v-btn>
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

const drawer = ref(false)

const lojaApi = new LojaApi();
const itens = ref([]);
const carrinho_itens = ref([])

const quantidade_item_carrinho = ref('')

onMounted(
  async function buscar() {
    itens.value = await lojaApi.buscarItens();
    carrinho_itens.value = await lojaApi.buscarCarrinho();
  }
)

const itemExists = ref(false)

// async function adicionarItemCarrinho(id) {
//   await lojaApi.adicionarCarrinho({
//     quantidade: 1,
//     item: id,
//   });
//   carrinho_itens.value = await lojaApi.buscarCarrinho();
// }

async function adicionarItemCarrinho(item) {
  itemExists.value = () => {
    for (let itemCarrinho of carrinho_itens.value) {
      if (itemCarrinho.item.id == item.id) {
        return true;
      }
    }
    return false;
  };
  if (itemExists.value()) {
    alert('Este item já está no carrinho!')
    return;
  } else {
    await lojaApi.adicionarCarrinho({
      quantidade: 1,
      item: item.id,
    });
  }
  carrinho_itens.value = await lojaApi.buscarCarrinho();
}

async function editarItem(item, valor) {
  if ( valor <= item.item.quantidade) {
    await lojaApi.EditarItemCarrinho(item.id, {
      quantidade: valor,
    });

    carrinho_itens.value = await lojaApi.buscarCarrinho();
  } else {
    console.log('a')
  }
}

async function removerItem(id) {
  await lojaApi.removerItemCarrinho(id);
  carrinho_itens.value = await lojaApi.buscarCarrinho();
}

// function estaNoCarrinho(id) {
//   for (let item of carrinho_itens.value) {
//     if (item.item.id == id) {
//       return true
//     } else {
//       return false
//     }
//   }
// }

</script>

<style scoped>
h2 {
  font-weight: 500;
  font-size: larger;
  text-align: center;
}

.item_carrinho {
  margin-top: 5px;
}

.excluir:hover {
  color: rgb(255, 54, 54);
  cursor: pointer;
}
</style>
