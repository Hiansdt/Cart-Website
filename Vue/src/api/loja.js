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
}
