import axios from "axios";
import { BASEURL } from "../Constants";

export const fetchGamestate = async (gameId = 1) => {
    try {
        const response = await axios.get(`${BASEURL}/get_gamestate`, { params: { game_id: gameId } });
        return response.data;
    } catch (error) {
        console.error(error);
    }
}