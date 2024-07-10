import axios from "axios";
import { BASEURL } from "../Constants";

export const postMakeMove = async (gameId = 1, row: number, col: string) => {
    try {
        const response = await axios.post(`${BASEURL}/make_move`, { game_id: gameId, row, col });
        return response.data;
    } catch (error) {
        console.error(error);
    }
}
