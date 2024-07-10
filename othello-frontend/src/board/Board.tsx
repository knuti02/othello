import { useEffect, useState } from "react";

import Square from "./Square";
import "./Board.css";

import { initGame } from "../api/initGame";
import { fetchLegalMoves } from "../api/fetchLegalMoves";
import { fetchGamestate } from "../api/fetchGamestate";
import { postMakeMove } from "../api/postMakeMove";

import { binToLst } from "../helper/binToLst";

import { GameData } from "../interface/GameData";
import { SquareData } from "../interface/SquareData";

const Board = () => {
  const [gameData, setGameData] = useState<GameData>({
    black_board: 0,
    white_board: 0,
    current_player: "",
    current_turn: 0,
    winner: "",
  });
  const [squareData, setSquareData] = useState<SquareData[]>([]);
  const [legalMoves, setLegalMoves] = useState<number[]>([]);

  const getLegalMoves = async () => {
    const legalMoves = await fetchLegalMoves();
    return legalMoves;
  };
  const updateGamestate = async () => {
    const gameData = await fetchGamestate();
    console.log(binToLst(gameData.black_board));
    setGameData(gameData);
  };

  // Initial fetch
  useEffect(() => {
    const init = async () => {
      const gameData = await initGame();
      console.log(binToLst(gameData.black_board));
      setGameData(gameData);
    };

    init();
  }, []);

  // Update legal moves when gameData changes
  useEffect(() => {
    //console.log("Gamedata updated!", gameData);
    const fetchLegalMoves = async () => {
      const legalMoves = await getLegalMoves();
      return binToLst(legalMoves);
    };

    fetchLegalMoves().then((data) => {
      //console.log(data);
      setLegalMoves(data);
    });
  }, [gameData]);

  // Update squareData when legalMoves changes
  useEffect(() => {
    const blackSquares = binToLst(gameData.black_board);
    const whiteSquares = binToLst(gameData.white_board);
    const squareData = Array.from({ length: 64 }, (_, i) => ({
      isEmpty: !blackSquares.includes(i) && !whiteSquares.includes(i),
      isLegalMove: legalMoves.includes(i),
      color: blackSquares.includes(i) ? "black" : "white",
      row: Math.floor(i / 8),
      col: String.fromCharCode(65 + (i % 8)),
    }));
    //console.log(squareData);
    setSquareData(squareData);
  }, [legalMoves]);

  const handleSquareClick = (index: number) => {
    const isValidPlacement = legalMoves.includes(index);
    if (!isValidPlacement) return;
    const row = Math.floor(index / 8);
    const column = String.fromCharCode(65 + (index % 8));
    console.log(row + column, isValidPlacement);

    postMakeMove(1, row, column).then(() => {
      console.log("Made move, new data");
      updateGamestate();
    });
  };

  return (
    <div className="board">
      {squareData.map((square, i) => (
        <Square
          key={i}
          isEmpty={square.isEmpty}
          isLegalMove={square.isLegalMove}
          color={square.color}
          row={square.row}
          col={square.col}
          onClick={() => handleSquareClick(i)}
        />
      ))}
    </div>
  );
};

export default Board;
