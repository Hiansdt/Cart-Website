import axios from "axios";

export default class LojaApi {
  async buscarItens() {
    const { data } = await axios.get("itens/");
    return data;
  }
  async enviarItem(Item) {
    const {data} = await axios.post("itens/", Item);
    return data;
  }
  async buscarCarrinho() {
    const {data} = await axios.get("carrinho_itens/");
    return data;
  }
  async adicionarCarrinho(item_carrinho) {
    const {data} = await axios.post("carrinho_itens/", item_carrinho);
    console.log(await axios.get(`itens/${item_carrinho.item}`).nome_item)
    return data;
  }
}
