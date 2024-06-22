
def wedge_eval(gamestate, player, opponent):
    """
    A wedge is a player's piece that is in the middle of two opponent's pieces in the edge
    """
    edges = 0b01111110_10000001_10000001_10000001_10000001_10000001_10000001_01111110
    wedge_modifier = 2
    potential_wedge_modifier = -1
    left_right_mask = 0b10000001_10000001_10000001_10000001_10000001_10000001_10000001_10000001
    up_down_mask = 0b11111111_00000000_00000000_00000000_00000000_00000000_00000000_11111111
    
    def evaluate_wedges(player, opponent):
        player_board = gamestate.board.get_board(player)
        player_edges = player_board & edges
        opponent_edges = gamestate.board.get_board(opponent) & edges
        
        player_potential_wedges = ((player_edges << 1 & player_edges >> 1 * left_right_mask) |
                                   (player_edges << 8 & player_edges >> 8 * up_down_mask))
        player_potential_wedges = bin(player_potential_wedges).count('1') * potential_wedge_modifier
        
        opponent_wedges = ((opponent_edges << 1 & opponent_edges >> 1 * left_right_mask) |
                           (opponent_edges << 8 & opponent_edges >> 8 * up_down_mask) & player_edges)
        opponent_wedges = bin(opponent_wedges).count('1') * wedge_modifier

        return player_potential_wedges + opponent_wedges
    
    player_wedges = evaluate_wedges(player, opponent)
    opponent_wedges = evaluate_wedges(opponent, player)
    
    wedge_denominator = abs(player_wedges) + abs(opponent_wedges)
    # prevent division by zero
    if wedge_denominator == 0:
        return 0
    
    combined_wedges_value = ((player_wedges - opponent_wedges) / (wedge_denominator))
    return combined_wedges_value