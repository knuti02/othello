
def danger_zones_eval(gamestate, player, opponent):
    orange_zone_penalty = -0.5
    red_zone_penalty = -5
    
    def evaluate_danger_zones(player, opponent) -> int:
        player_board = gamestate.board.get_board(player)
        all_occupied_corners = gamestate.board.corners & (player_board | gamestate.board.get_board(opponent))
        
        # Orange zones are the edge squares directly adjacent to the corners
        orange_zone = 0b01000010_10000001_00000000_00000000_00000000_00000000_10000001_01000010
        orange_zone = orange_zone & ~(all_occupied_corners << 1 | all_occupied_corners >> 1 | 
                                     all_occupied_corners << 8 | all_occupied_corners >> 8)
        # Red zones are the squares on the diagonals directly adjacent to the corners
        red_zone = 0b00000000_01000010_00000000_00000000_00000000_00000000_01000010_00000000
        red_zone = red_zone & ~(all_occupied_corners << 9 | all_occupied_corners >> 9 | 
                          all_occupied_corners << 7 | all_occupied_corners >> 7)
        
        orange_zone_value = bin(player_board & orange_zone).count('1')
        red_zone_value = bin(player_board & red_zone).count('1')
        
        return orange_zone_value * orange_zone_penalty + red_zone_value * red_zone_penalty
    
    player_danger_zones_value = evaluate_danger_zones(player, opponent)
    return player_danger_zones_value
    # opponent_danger_zones_value = evaluate_danger_zones(opponent, player)
    
    # danger_zones_denominator = abs(player_danger_zones_value) + abs(opponent_danger_zones_value)
    # # prevent division by zero
    # if danger_zones_denominator == 0:
    #     return 0
    
    # combined_danger_zones_value = 10 * ((player_danger_zones_value - opponent_danger_zones_value) / (danger_zones_denominator))
    # return combined_danger_zones_value