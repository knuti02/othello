package com.yourcompany;

import java.util.HashMap;
import java.util.ArrayList;

public class Square {
    final private int row;
    final private int col;
    private boolean isOccupied;
    private Color color;

    private ArrayList<Square> neighbors;
    private HashMap<Color, ArrayList<Square>> neighborMap; // key: Color, value: list of adjacent squares.
                                                           // effective way of finding adjacent squares, particularly
                                                           // those of opposing color which is needed for valid moves

    public Square(int row, int col, boolean isOccupied, Color color) {
        this.row = row;
        this.col = col;
        this.isOccupied = isOccupied;
        this.color = color;
        this.neighbors = new ArrayList<Square>();

        this.neighborMap = new HashMap<Color, ArrayList<Square>>();
        this.neighborMap.put(Color.EMPTY, new ArrayList<Square>());
        this.neighborMap.put(Color.BLACK, new ArrayList<Square>());
        this.neighborMap.put(Color.WHITE, new ArrayList<Square>());
    }

    // basic getters
    public int getRow() {
        return this.row;
    }

    public int getCol() {
        return this.col;
    }

    public boolean isOccupied() {
        return this.isOccupied;
    }

    public Color getColor() {
        return this.color;
    }

    public ArrayList<Square> getNeighbors() {
        return this.neighbors;
    }

    public HashMap<Color, ArrayList<Square>> getNeighborMap() {
        return this.neighborMap;
    }

    // basic setters
    public void setOccupied(boolean occupied) {
        this.isOccupied = occupied;
    }

    /*
     * Add a neighbor to the current square. The neighbor must be non-empty and not
     * already in the list.
     * This method also adds the neigbor to the neighbor map, regardless of wether
     * the square is empty or not.
     * 
     * @param neighbor The neighbor to be added to the current square.
     */
    public void addNeighbor(Square neighbor) throws IllegalArgumentException {
        if (neighbors.contains(neighbor)) {
            throw new IllegalArgumentException("Target square (neighbor) is already a neighbor of this square.");
        }

        this.getNeighbors().add(neighbor);
        this.getNeighborMap().get(neighbor.getColor()).add(neighbor);
    }

    /*
     * Set the color of the current square.
     * This method also updates the neighborMap of the current square's neighbors to
     * reflect the change in color for this square.
     * 
     * @param color The color to set the current square to.
     */
    public void setColor(Color color) {
        this.color = color;
        for (Square neighbor : this.getNeighbors()) {
            neighbor.updateNeighborMap(this);
        }
    }

    /*
     * Based on the square's position, determine the key which it is currently
     * occupying in the neighborMap.
     * 
     * @param neighbor The square to be updated in the neighborMap.
     */
    public Color getKeyFromSquare(Square neighbor) throws IllegalArgumentException {
        if (!neighbors.contains(neighbor)) {
            throw new IllegalArgumentException("Square is not a neighbor of this square.");
        }

        for (Color color : neighborMap.keySet()) {
            if (neighborMap.get(color).contains(neighbor)) {
                return color;
            }
        }
        return null; // should never be reached
    }

    /*
     * Updates the neighborMap of the current square.
     * This method assumes that the neighborMap of the current square has already
     * been initialized.
     * This method assumes that the incoming square has changed color, and must now
     * be updated in this square's map.
     * 
     * @param neighbor The square to be updated in the neighborMap.
     */
    public void updateNeighborMap(Square neighbor) {
        Color removeFrom = getKeyFromSquare(neighbor);
        // remove the neighbor from the neighborMap of the current color
        this.getNeighborMap().get(removeFrom).remove(neighbor);
        // add the neighbor to the neighborMap of the opposite color
        this.getNeighborMap().get(neighbor.getColor()).add(neighbor);
    }

    public String toString() {
        return this.getColor() + " square at (" + this.getRow() + "," + this.getCol() + ")";
    }

}
