def run_game(game_id, game, model_one, model_two, evaluation_function_one, evaluation_function_two, search_depth = 5, combination = None):
    model_one_player = game.current_player
    model_two_player = game.target_player
    
    agent = {
        model_one_player : {'model' : model_one, 'eval_func' : evaluation_function_one}, 
        model_two_player : {'model' : model_two, 'eval_func' : evaluation_function_two}
    }
    
    game_states = []
    moves = []
    game_results = {
        'FinalScore' : 0, 'Winner' : 0
    }
    
    while not game.game_over:
        current_agent = agent[game.current_player]
        _, move = current_agent['model'].get_best_move(game, current_agent['eval_func'], search_depth)
        current_agent['model'].clear_cache()
        
        MoveID = (int(game_id) << 8) | int(game.current_turn)
        MoveNumber = game.current_turn
        Player = game.current_player
        Move = str(move)
        
        moves.append({
            'MoveID' : MoveID,
            'GameID' : game_id,
            'MoveNumber' : MoveNumber,
            'Player' : Player,
            'Move' : Move
        })
        
        GameStateID = (int(game_id) << 8) | int(game.current_turn)
        CurrentPlayer = Player
        MoveNumber = MoveNumber
        PiecesPlaced = bin(game.board.get_board(model_one_player)).count('1') + bin(game.board.get_board(model_two_player)).count('1')
        
        heuristics = current_agent['eval_func'](game, game.current_player, game.target_player, return_heuristics = True)
        CombinedScore = heuristics['combined']
        MobilityScore = heuristics['mobility']
        StabilityScore = heuristics['stability']
        CoinsScore = heuristics['coins']
        CornersScore = heuristics['corners']
        DangerZonesScore = heuristics['danger_zones']
        EdgesScore = heuristics['edges']
        WedgesScore = heuristics['wedges']
        
        CurrentPlayerBitboard = str(game.board.board[game.current_player])
        OpponentBitboard = str(game.board.board[game.target_player])
        
        game_states.append({
            'GameStateID' : GameStateID,
            'GameID' : game_id,
            'CurrentPlayer' : CurrentPlayer,
            'MoveNumber' : MoveNumber,
            'PiecesPlaced' : PiecesPlaced,
            'CombinedScore' : CombinedScore,
            'MobilityScore' : MobilityScore,
            'StabilityScore' : StabilityScore,
            'CoinsScore' : CoinsScore,
            'CornersScore' : CornersScore,
            'DangerZonesScore' : DangerZonesScore,
            'EdgesScore' : EdgesScore,
            'WedgesScore' : WedgesScore,
            'CurrentPlayerBitboard' : CurrentPlayerBitboard,
            'OpponentBitboard' : OpponentBitboard
        })
        
        if move == "skip":
            game.skip_turn()
        else:
            game.make_move(move[0], move[1])
                        
    final_socre = str(bin(game.board.get_board(model_one_player)).count('1')) + "-" + str(bin(game.board.get_board(model_two_player)).count('1'))
    winner = game.winner
    
    if winner == model_one_player and combination is not None:
        print("Winner: " + winner)
        print(game.board)
        print("Combination used:")
        print(combination)
    
    game_results['FinalScore'] = final_socre
    game_results['Winner'] = winner
    
    return {
        'game_states' : game_states,
        'moves' : moves,
        'game_results' : game_results
    }