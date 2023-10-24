def give_game_id(game_log):
    """Given a game_log_array, returns the game_id from that array
    Input: LeagueGameLog (see above)
    Output: '0022201230'
    """
    game_id = game_log[4]
    return game_id