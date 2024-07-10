import axios from "axios";
import { BASEURL } from "../Constants";

export const initGame = async (gameId = 1) => {
  try {
    const response = await axios.post(`${BASEURL}/init`, { game_id: gameId });
    return response.data;
  } catch (error) {
    console.error(error);
  }
};