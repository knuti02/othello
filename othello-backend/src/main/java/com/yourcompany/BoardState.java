package com.yourcompany;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Scanner;

public class BoardState {
    private OthelloBoard board;
    private Color currentPlayer;
    private HashMap<Color, ArrayList<Square>> placesPiecesMap;

    public BoardState(OthelloBoard board, Color currentPlayer) {
        this.board = board;
        this.currentPlayer = currentPlayer;
        this.placesPiecesMap = new HashMap<>();
        this.placesPiecesMap.put(Color.BLACK, new ArrayList<>());
        this.placesPiecesMap.put(Color.WHITE, new ArrayList<>());
    }

    private void init() {
        // set the initial pieces' color
        this.board.getSquare(3, 3).setColor(Color.WHITE);
        this.board.getSquare(3, 4).setColor(Color.BLACK);
        this.board.getSquare(4, 3).setColor(Color.BLACK);
        this.board.getSquare(4, 4).setColor(Color.WHITE);

        // add the squares to the map
        this.placesPiecesMap.get(this.board.getSquare(3, 3).getColor()).add(this.board.getSquare(3, 3));
        this.placesPiecesMap.get(this.board.getSquare(3, 4).getColor()).add(this.board.getSquare(3, 4));
        this.placesPiecesMap.get(this.board.getSquare(4, 3).getColor()).add(this.board.getSquare(4, 3));
        this.placesPiecesMap.get(this.board.getSquare(4, 4).getColor()).add(this.board.getSquare(4, 4));

    }

    // public methods
    public HashSet<Square> getValidMoves() {
        HashSet<Square> initValidMoves = new HashSet<>();
        Color targetColor = this.currentPlayer == Color.BLACK ? Color.WHITE : Color.BLACK;

        // Populate initial valid moves
        populateInitialValidMoves(initValidMoves, targetColor);

        // Filter valid moves away
        return filterFinalValidMoves(initValidMoves, targetColor);
    }

    public void placePiece(int row, int col) throws IllegalArgumentException {
        Color targetColor = this.currentPlayer == Color.BLACK ? Color.WHITE : Color.BLACK;
        Square square = this.board.getSquare(row, col);
        if (!getValidMoves().contains(square))
            throw new IllegalArgumentException("Not a valid move!");

        square.setColor(this.currentPlayer);
        this.placesPiecesMap.get(this.currentPlayer).add(square);
        for (Square neighbor : square.getNeighbors()) {
            Directions direction = this.board.getDirectionOfNeighbor(square, neighbor);
            if (canFlankInDirection(neighbor, direction, targetColor)) {
                flipPieces(square, direction, targetColor);
            }
        }

        this.setPlayer(targetColor);
    }

    // private methods
    private void populateInitialValidMoves(HashSet<Square> initValidMoves, Color targetColor) {
        // instead of looping through every cell in the board, only loop through those
        // which are empty neighbors of opposing color
        for (Square square : this.placesPiecesMap.get(targetColor)) {
            initValidMoves.addAll(square.getNeighborMap().get(Color.EMPTY));
        }
    }

    private HashSet<Square> filterFinalValidMoves(HashSet<Square> initValidMoves, Color targetColor) {
        HashSet<Square> finalValidMoves = new HashSet<>();
        // go through every (initial) valid move
        for (Square square : initValidMoves) {
            // see if qualifies as an actual valid move
            if (isValidMove(square, targetColor)) {
                finalValidMoves.add(square);
            }
        }
        return finalValidMoves;
    }

    private boolean isValidMove(Square square, Color targetColor) {
        // go through all neighbors of square
        ArrayList<Square> neighbors = square.getNeighborMap().get(targetColor);
        for (Square neighbor : neighbors) {
            // find the direction to the neighbor
            Directions direction = this.board.getDirectionOfNeighbor(square, neighbor);
            // see if you can flank in this direction, if so it is a valid move
            if (canFlankInDirection(neighbor, direction, targetColor)) {
                return true;
            }
        }
        return false;
    }

    private boolean canFlankInDirection(Square startSquare, Directions direction, Color targetColor) {
        Square currentSquare = startSquare;
        // go through every square in this direction until you either hit an
        // empty square / border (false), or your own square (true)
        while (true) {
            currentSquare = this.board.getNeighboringSquareDirection(currentSquare, direction);
            // hit wall or empty square; not valid
            if (currentSquare == null || currentSquare.getColor() == Color.EMPTY) {
                return false;
            }
            // hit another target color; continue
            else if (currentSquare.getColor() == targetColor) {
                continue;
            }
            return true; // Hit the player's color; valid
        }
    }

    private void flipPieces(Square startSquare, Directions direction, Color targetColor) {
        Square currentSquare = startSquare;
        while (true) {
            currentSquare = this.board.getNeighboringSquareDirection(currentSquare, direction);
            if (currentSquare.getColor() == targetColor) {
                currentSquare.setColor(this.currentPlayer);
                this.placesPiecesMap.get(targetColor).remove(currentSquare);
                this.placesPiecesMap.get(this.currentPlayer).add(currentSquare);
            } else
                return;
        }
    }

    private void setPlayer(Color color) {
        this.currentPlayer = color;
    }

    public static void main(String[] args) {
        OthelloBoard othelloBoard = new OthelloBoard(8, 8);
        BoardState game = new BoardState(othelloBoard, Color.BLACK);
        game.init();
        Scanner scanner = new Scanner(System.in);
        System.out.println(game.board);
        while (true) {
            System.out.println("Valid moves: " + game.getValidMoves());
            System.out.println("Choose square to place (row,col)");
            String coords = scanner.nextLine();
            String[] parts = coords.split(",");
            int row = Integer.parseInt(parts[0].trim());
            int col = Integer.parseInt(parts[1].trim());
            game.placePiece(row, col);
            System.out.println(game.board);
        }

    }
}
