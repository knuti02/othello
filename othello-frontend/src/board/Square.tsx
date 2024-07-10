import { useEffect } from "react";
import blackChip from "../assets/blackChip.svg";
import whiteChip from "../assets/whiteChip.svg";
import { useHover } from "@uidotdev/usehooks";
import "./Square.css";

interface SquareProps {
  isEmpty: boolean;
  isLegalMove: boolean;
  color: string;
  row: number;
  col: string;
  onClick: () => void;
}

const Square = ({
  isEmpty,
  isLegalMove,
  color,
  row,
  col,
  onClick,
}: SquareProps) => {
  const [hoverRef, isHovered] = useHover();
  const chip = color === "black" ? blackChip : whiteChip;

  useEffect(() => {
    if (isHovered) {
      console.log(color, row + col);
    }
  }, [isHovered]);

  const handleClick = () => {
    onClick();
  };

  return (
    <>
      {!isEmpty ? (
        <img src={chip} alt={color} ref={hoverRef} className="square" />
      ) : (
        <div
          className={`square ${isLegalMove ? "legalMove" : ""}`}
          onClick={handleClick}
        />
      )}
    </>
  );
};

export default Square;
