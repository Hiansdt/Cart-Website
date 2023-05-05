<template>
  <v-app id="inspire">

    <v-navigation-drawer v-model="drawer" class="drawer" right>
      <h2>Carrinho</h2>
      <v-card v-for="item in carrinho_itens" :key="item.id" class="item_carrinho">
        {{ item.item.nome_item }}
        ({{ item.quantidade }})
        <v-icon @click="removerItem(item.id)" class="excluir">mdi-delete</v-icon>
        <v-icon class="aumentar" @click="editarItem(item, item.quantidade += 1)"> mdi-plus </v-icon>
        <v-icon class="diminuir" @click="editarItem(item, item.quantidade -= 1)"> mdi-minus </v-icon>
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
          <div class="item" v-for="item in itens" :key="item.id">
            <p class="nome">{{ item.nome_item }}</p>
            <div class="info">
              <img :src="item.foto.url" alt="" height="150" width="150">
              <p>Estoque: {{ item.quantidade }}</p>
              <P class="preco">R$ {{ item.valor }}</P>
              <v-btn @click="adicionarItemCarrinho(item)">Adicionar ao carrinho</v-btn>
            </div>
          </div>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>


<script setup>

import LojaApi from '@/api/loja';
import { ref, onMounted } from "vue";
import Swal from 'sweetalert2'

const drawer = ref(false)

const lojaApi = new LojaApi();
const itens = ref([]);
const carrinho_itens = ref([])

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
    Swal.fire('Este item já está no carrinho!')
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
  if (valor <= item.item.quantidade) {

    if (valor > 0) {
      await lojaApi.EditarItemCarrinho(item.id, {
        quantidade: valor,
      });

      carrinho_itens.value = await lojaApi.buscarCarrinho();
    } else {
      Swal.fire({
        title: 'Aviso',
        text: 'Deseja remover o item do carrinho?',
        icon: 'warning',
        confirmButtonText: 'Remover do carrinho',
        cancelButtonText: 'Cancelar',
        showCancelButton: true,
      }).then(function (result) {
        if (result.isConfirmed) {
          removerItem(item.id)
        } else if (result.isDenied) {
          alert('a')
        }
      })
      carrinho_itens.value = await lojaApi.buscarCarrinho();
    }
  } else {
    console.log('a')
    carrinho_itens.value = await lojaApi.buscarCarrinho();
  }
}

async function removerItem(id) {
  await lojaApi.removerItemCarrinho(id);
  carrinho_itens.value = await lojaApi.buscarCarrinho();
}

</script>

<style scoped>
h2 {
  font-weight: 500;
  font-size: larger;
  text-align: center;
}

.preco {
  background-color: rgb(0, 221, 0);
  width: 110px;
  height: 25px;
  text-align: center;
  border-radius: 10px;
  margin: 10px;
}
.info {
  display: flex;
  align-items: center;
}

.nome {
  text-align: center;
  font-weight: bold;
  font-size: larger;
}

.aumentar {
  color: rgb(34, 229, 255);
}

.diminuir {
  color: rgb(211, 0, 105);
}

.item {
  margin: 10px;
  align-items: center;
  justify-content: center;
  width: 45%;
  background-color: aliceblue;
}

.item_carrinho {
  margin-top: 5px;
  background-color: rgb(194, 194, 194);
}

.excluir:hover {
  color: rgb(255, 54, 54);
  cursor: pointer;
}
</style>
