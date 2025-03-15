import math
from constants import WEDGES_WEDGE_WEIGHT, WEDGES_POTENTIAL_WEIGHT, WEDGES_STANDARD_WEIGHT, WEDGES_DYNAMIC_MAX_WEIGHT, WEDGES_DYNAMIC_MIDPOINT, WEDGES_DYNAMIC_STEEPNESS

def wedge_heuristics_weight_function(
        placed_pieces: int, 
        maximum_weight: int = WEDGES_DYNAMIC_MAX_WEIGHT,  
        midpoint: int = WEDGES_DYNAMIC_MIDPOINT, 
        steepness: float = WEDGES_DYNAMIC_STEEPNESS
    ) -> float:
    """
    Computes a dynamic weight for wedge evaluation using a sigmoid function.
    In the early game (low placed_pieces), the weight is low.
    As the game progresses, the weight approaches maximum_weight.
    """
    return maximum_weight / (1 + math.e ** (-steepness * (placed_pieces - midpoint)))


def wedges_eval(gamestate, player, opponent, placed_pieces, dynamic_weight=True):
    """
    Evaluates wedge formations.
    
    A wedge is defined here as a player's piece on an edge that is flanked 
    horizontally (or vertically) by opponent pieces—meaning it is locked in 
    and cannot be flipped unless the player moves it.
    
    The function computes a normalized wedge score and multiplies it by a dynamic weight,
    which increases as more pieces are placed on the board.
    """
    # Modifiers for wedge calculations
    wedge_modifier = WEDGES_WEDGE_WEIGHT
    potential_wedge_modifier = WEDGES_POTENTIAL_WEIGHT
    
    # Bitboard for edges (for an 8x8 board)
    edges = 0b01111110_10000001_10000001_10000001_10000001_10000001_10000001_01111110
    
    # Masks to help evaluate horizontal vs. vertical configurations
    left_right_mask = 0b10000001_10000001_10000001_10000001_10000001_10000001_10000001_10000001
    up_down_mask    = 0b11111111_00000000_00000000_00000000_00000000_00000000_00000000_11111111
    
    def evaluate_wedges(player, opponent):
        player_board = gamestate.board.get_board(player)
        # Restrict to pieces on the edge
        player_edges = player_board & edges
        opponent_edges = gamestate.board.get_board(opponent) & edges
        
        # Calculate potential wedges:
        # For horizontal wedges, a simple idea is to shift left and right and combine with a mask.
        # (Be cautious with operator precedence; you might need extra parentheses if the expression is complex.)
        horizontal_wedges = (player_edges << 1) & (player_edges >> 1) & left_right_mask
        vertical_wedges = (player_edges << 8) & (player_edges >> 8) & up_down_mask
        
        player_potential_wedges = (bin(horizontal_wedges).count('1') + bin(vertical_wedges).count('1')) * potential_wedge_modifier
        
        # For opponent wedges, we look for similar patterns (and possibly consider interference with player's pieces)
        opponent_horizontal = (opponent_edges << 1) & (opponent_edges >> 1) & left_right_mask
        opponent_vertical   = (opponent_edges << 8) & (opponent_edges >> 8) & up_down_mask
        opponent_wedges = (bin(opponent_horizontal).count('1') + bin(opponent_vertical).count('1')) * wedge_modifier
        
        return player_potential_wedges + opponent_wedges

    # Compute wedge scores for each side
    player_wedges = evaluate_wedges(player, opponent)
    opponent_wedges = evaluate_wedges(opponent, player)
    
    wedge_denominator = abs(player_wedges) + abs(opponent_wedges)
    if wedge_denominator == 0:
        return 0
    
    # Base wedge score is normalized difference.
    base_wedge_score = (player_wedges - opponent_wedges) / wedge_denominator
    
    # Apply dynamic weighting
    weight = wedge_heuristics_weight_function(placed_pieces) if dynamic_weight else WEDGES_STANDARD_WEIGHT
    combined_wedges_value = weight * base_wedge_score
    
    return combined_wedges_value
