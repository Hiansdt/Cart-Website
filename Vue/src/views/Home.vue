<template>
  <v-app id="inspire">

    <v-navigation-drawer v-model="drawer" class="drawer" right>
      <h2>Carrinho | Total: {{ total }}</h2>
      <div v-for="item in carrinho_itens" :key="item.id" class="item_carrinho">
        <v-icon class="carrinho_icone">mdi-hanger</v-icon>
        {{ item.item.nome_item }}
        <div class="quantidade">
          <v-icon class="quantidade-btn" size="20" @click="editarItem(item, item.quantidade += 1)"> mdi-chevron-up
          </v-icon>
          {{ item.quantidade }}
          <v-icon class="quantidade-btn" size="20" @click="editarItem(item, item.quantidade -= 1)"> mdi-chevron-down
          </v-icon>
        </div>
        <v-icon @click="removerItem(item.id)" class="excluir">mdi-delete</v-icon>
      </div>
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
              <img :src="item.foto.url" alt="" class="imagem">
              <p>Estoque: {{ item.quantidade }}</p>
              <P class="preco">R$ {{ item.valor }}</P>
              <v-btn @click="adicionarItemCarrinho(item)" class="add">Adicionar ao carrinho</v-btn>
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
    calcularTotal()
  }
)

const total = ref(0)

function calcularTotal() {
  total.value = 0.00;
  for (let item of carrinho_itens.value) {
    total.value += item.quantidade * item.item.valor;
  }
  total.value = total.value.toFixed(2);
}

calcularTotal();

const itemExists = ref(false)

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
  calcularTotal();
}

async function editarItem(item, valor) {
  if (valor <= item.item.quantidade) {

    if (valor > 0) {
      await lojaApi.EditarItemCarrinho(item.id, {
        quantidade: valor,
      });

      carrinho_itens.value = await lojaApi.buscarCarrinho();
      calcularTotal();
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
      calcularTotal();
    }
  } else {
    console.log('a')
    carrinho_itens.value = await lojaApi.buscarCarrinho();
  }
}

async function removerItem(id) {
  await lojaApi.removerItemCarrinho(id);
  carrinho_itens.value = await lojaApi.buscarCarrinho();
  calcularTotal();
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
  width: 20%;
  height: 5%;
  text-align: center;
  border-radius: 10px;
  margin: 1%;
}

.carrinho_icone {
  margin-right: 30px;
}

.quantidade {
  display: flex;
  flex-direction: column;
  margin-left: 20px;
  text-align: center;
}

.info {
  display: flex;
  align-items: center;
}

.imagem {
  height: 100px;
  width: 100px;
}

.nome {
  text-align: center;
  font-weight: bold;
  font-size: larger;
}

.add {
  width: 40%;
  font-size: 80%;
}

.quantidade-btn {
  size: x-small;
}

.item {
  margin: 1%;
  align-items: center;
  justify-content: center;
  width: 45%;
  background-color: aliceblue;
}

.item_carrinho {
  margin-top: 5px;
  background-color: rgb(194, 194, 194);
  display: flex;
  align-items: center;
  justify-content: center;
}

.excluir:hover {
  color: rgb(255, 54, 54);
  cursor: pointer;
}

.excluir {
  margin-left: 20px;
}
</style>
