<template>
  <v-app id="inspire">

    <v-navigation-drawer v-model="drawer" class="drawer" right>
      <h2>Carrinho</h2>
      <div v-for="item in carrinho_itens" :key="item.id" class="item_carrinho">
        <v-icon class="carrinho_icone">mdi-hanger</v-icon>
        <p class="nome_item_carrinho">{{ item.item.nome_item }}</p>
        <div class="quantidade">
          <v-icon class="quantidade-btn" size="20" @click="editarItem(item, item.quantidade += 1)"> mdi-chevron-up
          </v-icon>
          <p>{{ item.quantidade }}</p>
          <v-icon class="quantidade-btn" size="20" @click="editarItem(item, item.quantidade -= 1)"> mdi-chevron-down
          </v-icon>
        </div>
        <p class="preco_item_carrinho"> R$ {{ (item.quantidade * item.item.valor).toFixed(2) }} </p>
        <v-icon @click="removerItem(item.id)" class="excluir">mdi-delete</v-icon>
      </div>
    </v-navigation-drawer>

    <v-app-bar app>

      <v-btn icon>

        <v-icon @click="drawer = !drawer" size="50">
          mdi-cart
        </v-icon>

      </v-btn>

      <v-toolbar-title class="titulo">Cavalo Variedades <v-icon> mdi-horse-variant </v-icon> </v-toolbar-title>

      <v-icon size="50"> mdi-account </v-icon>
    </v-app-bar>

    <v-main>
      <v-container>
        <v-row>
          <div class="item" v-for="item in itens" :key="item.id">
            <div class="item_inside">
              <img :src="item.foto.url" alt="" class="imagem">
              <div class="info">
                <p class="nome">{{ item.nome_item }}</p>
                <p>Estoque: {{ item.quantidade }}</p>
                <P class="preco">R$ {{ item.valor }}</P>
                <v-btn @click="adicionarItemCarrinho(item)" class="add">Adicionar ao carrinho</v-btn>
              </div>
            </div>
          </div>
        </v-row>
      </v-container>
    </v-main>
    <div class="total">
      <p>Total: {{ total }}</p>
    </div>
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
.titulo {
  font-family: 'lato' !important;
  text-align: center;
  font-size: xx-large !important;
}

h2 {
  font-weight: 500;
  font-size: larger;
  text-align: center;
}

.preco {
  width: 50%;
  height: 20%;
  text-align: center;
  border-radius: 15px;
  margin: 1%;
  font-weight: bold;
  background-color: #ffffff;
  box-shadow: 1px 1px 5px;
}

.item_inside {
  padding: 2%;
}

.v-toolbar-title {
  font-weight: 500;
  font-size: x-large;
}

.total {
  position: fixed;
  background-color: #F8CBA6;
  bottom: 10px;
  right: 10px;
  width: fit-content;
  border-radius: 20px;
  font-size: larger;
  font-weight: 700;
  padding: 5px;
}

.carrinho_icone {
  position: fixed;
  left: 5%;
}

.nome_item_carrinho {
  position: fixed;
  left: 17%;
}

.preco_item_carrinho {
  position: fixed;
  left: 60%;
}

.quantidade {
  display: flex;
  flex-direction: column;
  margin-left: 10px;
  margin-right: 10px;
  text-align: center;
  position: fixed;
  left: 40%;
}

.info {
  display: flex;
  align-items: center;
  flex-direction: column;
}

.imagem {
  height: 200px;
  width: 200px;
}

.nome {
  text-align: center;
  font-weight: bold;
  font-size: larger;
}

.add {
  width: 90%;
  font-size: 80%;
}

.quantidade-btn {
  size: x-small;
}

.item {
  margin: 1%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-evenly;
  width: 45%;
  background-color: #f0f0f0;
  box-shadow: 5px 5px 5px grey;
}

.item_carrinho {
  margin-top: 5px;
  background-color: #F8CBA6;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 5px;
  margin-right: 5px;
  height: 8%;
}

.excluir:hover {
  color: rgb(255, 54, 54);
  cursor: pointer;
}

.excluir {
  position: fixed;
  right: 2%;
}
</style>
