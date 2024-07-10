import Square from "./Square";
import "./Board.css";
import { useState } from "react";

const Board = () => {
  const [squaresData, setSquaresData] = useState<
    Array<{ isEmpty: boolean; color: string }>
  >(
    Array.from({ length: 64 }, (_, i) => ({
      // black squares at 28 and 35 and white squares at 27 and 36
      isEmpty: i !== 27 && i !== 36 && i !== 28 && i !== 35,
      color: i === 28 || i === 35 ? "black" : "white",
    }))
  );

  const handleSquareClick = (index: number) => {
    // translate to row and column where row is from 0 to 7 and column from A to H
    const row = Math.floor(index / 8);
    const column = String.fromCharCode(65 + (index % 8));
    console.log(`Square clicked: ${column}${row}`);
  };

  return (
    <div className="board">
      {squaresData.map((square, i) => (
        <Square
          key={i}
          isEmpty={square.isEmpty}
          color={square.color}
          onClick={() => handleSquareClick(i)}
        />
      ))}
    </div>
  );
};

export default Board;
