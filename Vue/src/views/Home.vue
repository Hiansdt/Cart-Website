<template>
  <v-app id="inspire">

    <v-navigation-drawer v-model="drawer" class="drawer" :width="400" floating>
      <div class="carrinho_nome">
        <h2>Carrinho</h2>
        <p class="total">Total: R$ {{ total }}</p>
      </div>
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
    Swal.fire({
      text: "Este Item já está no carrinho!",
      confirmButtonText: "Entendido",
      confirmButtonColor: 'black',
    })
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
        cancelButtonColor: 'grey',
        confirmButtonColor: 'black',
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

.carrinho_nome {
  font-weight: 500;
  font-size: small;
  text-align: center;
  font-family: 'lato';
  font-weight: 600;
  justify-content: center;
  align-items: center;
  display: flex;
  flex-direction: column;
  box-shadow: 0px 4px 5px rgb(156, 156, 156);
  height: 64px;
  border-right: 1px solid grey;
}


.preco {
  width: 50%;
  height: 20%;
  text-align: center;
  border-radius: 15px;
  margin: 1%;
  font-weight: bold;
  background-color: #2e2e2e;
  color: white;
}

.item_inside {
  padding: 2%;
}

.v-toolbar-title {
  font-weight: 500;
  font-size: x-large;
}

.total {
  background-color: #000000;
  color: white;
  width: fit-content;
  border-radius: 20px;
  font-size: small;
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
  border-bottom: 1px solid;
}

.nome {
  text-align: center;
  font-weight: bold;
  font-size: larger;
}

.add {
  width: 90%;
  font-size: 80%;
  background-color: #131313;
  color: white;
}

.add:hover {
  transform: scale(1.05);
}

.quantidade-btn {
  size: x-small;
}

.quantidade-btn:hover {
  transform: scale(1.15);
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
  margin: 15px;
  background-color: #ffffff;
  color: rgb(0, 0, 0);
  display: flex;
  align-items: center;
  justify-content: center;
  height: 7%;
  font-family: 'Times New Roman', Times, serif;
  font-weight: 600;
  box-shadow: 2px 2px 5px rgb(83, 83, 83);
}

.excluir:hover {
  color: rgb(255, 54, 54);
  cursor: pointer;
  transform: scale(1.2);
}

.excluir {
  position: fixed;
  right: 5%;
}
</style>
