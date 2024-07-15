import axios from "axios";
import { BASEURL } from "../Constants";

export const fetchLegalMoves = async (gameId = 1) => {
  try {
    const response = await axios.get(`${BASEURL}/get_legal_moves`, { params: { game_id: gameId } });
    console.log(response.data.toString(2));
    return response.data;
  } catch (error) {
    console.error(error);
  }
};