import { useEffect } from "react";
import blackChip from "../assets/blackChip.svg";
import whiteChip from "../assets/whiteChip.svg";
import { useHover } from "@uidotdev/usehooks";
import "./Square.css";

interface SquareProps {
  isEmpty: boolean;
  color: string;
  onClick: () => void;
}

const Square = ({ isEmpty, color, onClick }: SquareProps) => {
  const [hoverRef, isHovered] = useHover();
  const chip = color === "black" ? blackChip : whiteChip;

  useEffect(() => {
    console.log(isHovered, color);
  }, [isHovered]);

  const handleClick = () => {
    onClick();
  };

  return (
    <>
      {!isEmpty ? (
        <img src={chip} alt={color} ref={hoverRef} className="square" />
      ) : (
        <div className="square" onClick={handleClick} />
      )}
    </>
  );
};

export default Square;
