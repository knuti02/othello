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
    if (isHovered && !isEmpty) {
      console.log("Placed piece", color, row + col);
    } else if (isHovered && isLegalMove) {
      console.log("Legal move", color, row + col);
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
          ref={hoverRef}
        >
          {isLegalMove && isHovered && (
            <img src={chip} alt={color} className="faded" />
          )}
        </div>
      )}
    </>
  );
};

export default Square;
