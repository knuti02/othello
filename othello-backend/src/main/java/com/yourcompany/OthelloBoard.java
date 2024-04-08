package com.yourcompany;

import java.util.HashMap;

public class OthelloBoard {
    private Square[][] boardDimension;
    private HashMap<Directions, Integer[]> directionMap;

    public OthelloBoard(int y, int x) {
        boardDimension = new Square[y][x];

        for (int row = 0; row < y; row++) {
            for (int col = 0; col < x; col++) {
                boardDimension[row][col] = new Square(row, col, false, Color.EMPTY);
            }
        }

        // add neighbors
        for (int row = 0; row < y; row++) {
            for (int col = 0; col < x; col++) {
                Square currentSquare = this.getSquare(row, col);
                for (int i = -1; i <= 1; i++) {
                    for (int j = -1; j <= 1; j++) {
                        if (i == 0 && j == 0)
                            continue;
                        if (row + i < 0 || row + i >= y || col + j < 0 || col + j >= x)
                            continue;
                        currentSquare.addNeighbor(this.getSquare(row + i, col + j));
                    }
                }
            }
        }

        directionMap = new HashMap<>();
        directionMap.put(Directions.NORTH, new Integer[] { 1, 0 });
        directionMap.put(Directions.SOUTH, new Integer[] { -1, 0 });
        directionMap.put(Directions.EAST, new Integer[] { 0, 1 });
        directionMap.put(Directions.WEST, new Integer[] { 0, -1 });
        directionMap.put(Directions.NORTH_EAST, new Integer[] { 1, 1 });
        directionMap.put(Directions.NORTH_WEST, new Integer[] { 1, -1 });
        directionMap.put(Directions.SOUTH_EAST, new Integer[] { -1, 1 });
        directionMap.put(Directions.SOUTH_WEST, new Integer[] { -1, -1 });

    }

    public Square[][] getBoardDimension() {
        return boardDimension;
    }

    public Square getSquare(int row, int col) {
        try {
            return boardDimension[row][col];
        } catch (IndexOutOfBoundsException e) {
            return null;
        }
    }

    public Square getNeighboringSquareDirection(Square square, Directions direction) {
        Integer[] dir = directionMap.get(direction);
        return getSquare(square.getRow() + dir[0], square.getCol() + dir[1]);
    }

    public Directions getDirectionOfNeighbor(Square origin, Square target) {
        int x = target.getRow() - origin.getRow();
        int y = target.getCol() - origin.getCol();

        // ugly code but is needed because of the way the directions are stored
        if (x == 1 && y == 0) {
            return Directions.NORTH;
        } else if (x == -1 && y == 0) {
            return Directions.SOUTH;
        } else if (x == 0 && y == 1) {
            return Directions.EAST;
        } else if (x == 0 && y == -1) {
            return Directions.WEST;
        } else if (x == 1 && y == 1) {
            return Directions.NORTH_EAST;
        } else if (x == 1 && y == -1) {
            return Directions.NORTH_WEST;
        } else if (x == -1 && y == 1) {
            return Directions.SOUTH_EAST;
        } else if (x == -1 && y == -1) {
            return Directions.SOUTH_WEST;
        }
        return null; // should be unreachable
    }

    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < boardDimension.length; i++) {
            sb.append("|");
            for (int j = 0; j < boardDimension[i].length; j++) {
                sb.append(boardDimension[i][j].getColor().toString() + "|");
            }
            sb.append("\n");
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        OthelloBoard board = new OthelloBoard(8, 8);
        System.out.println(board.getSquare(0, 0).getNeighbors());
    }
}
