import axios from "axios";

export default class ItensApi {
  async buscarItens() {
    const { data } = await axios.get("itens/");
    return data;
  }
}
