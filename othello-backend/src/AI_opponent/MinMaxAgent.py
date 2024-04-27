import copy

def MinMaxAgent(gamestate, heuristic_function, max_depth, alpha=-float('inf'), beta=float('inf'), cache={}, is_maximizing=True, player=None):
    best_move = None

    for depth in range(1, max_depth + 1):
        value, move = min_max_with_depth(gamestate, heuristic_function, depth, alpha, beta, cache, is_maximizing, player)
        if move is not None:
            best_move = move

    return value, best_move

def min_max_with_depth(gamestate, heuristic_function, depth, alpha, beta, cache, is_maximizing, player):
    # Base case
    if depth == 0 or gamestate.is_game_over():
        value = heuristic_function(gamestate, player)
        return value, None

    player = gamestate.current_player
    # Represent the gamestate as a string of the pieces' names
    # Used for caching
    board = ''.join([square.color.name for row in gamestate.board.board_dimension for square in row])  # Compact way to create the board string
    if board in cache:
        depth_searched, value, best_move = cache[board]
        if depth_searched >= depth:
            return value, best_move

    max_value = float('-inf')
    min_value = float('inf')
    best_move = None

    valid_moves = gamestate.get_valid_moves(player)

    for move in valid_moves:
        gamestate_copy = copy.deepcopy(gamestate)
        if move == "skip":
            gamestate_copy.skip_turn()
        else:
            gamestate_copy.place_piece(move.row, move.col)
        gamestate_copy.next_turn()
        value, _ = min_max_with_depth(gamestate_copy, heuristic_function, depth - 1, alpha, beta, cache, not is_maximizing, player)

        if is_maximizing:
            if value > max_value:
                max_value = value
                best_move = move
            alpha = max(max_value, value)
        else:
            if value < min_value:
                min_value = value
                best_move = move
            beta = min(min_value, value)

        if beta <= alpha:
            break

    if is_maximizing:
        cache[board] = depth, max_value, best_move
        return max_value, best_move
    else:
        cache[board] = depth, min_value, best_move
        return min_value, best_move
