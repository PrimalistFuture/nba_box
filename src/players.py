from nba_api.stats.endpoints import boxscoretraditionalv2
from datetime import date
from games import give_games_of_the_past_week, give_game_id

# PlayerStats': ['GAME_ID','TEAM_ID','TEAM_ABBREVIATION','TEAM_CITY','PLAYER_ID','PLAYER_NAME','START_POSITION','COMMENT','MIN','FGM','FGA','FG_PCT','FG3M','FG3A','FG3_PCT','FTM','FTA','FT_PCT','OREB','DREB','REB','AST','STL','BLK','TO','PF','PTS','PLUS_MINUS']

def player_data_from_id(game_id_string, player_info=None):
    """Given a game_id string and optionally some player info, returns the game data of that player, or all game data if no player info is supplied.
    Input: game_id string like '0022201230', player info like 'Stephen Curry' or 201939 (notice that player id is not a string, but game_id is)
    Output: PlayerStats (see above)
    """

    if type(game_id_string) is not str:
        return f'{game_id_string} must be a string.'

    if len(game_id_string) != 10:
        return f'{game_id_string} is not a valid game_id. Ensure the the game_id has a length of 10.'

    game_response = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id_string).get_dict()

    if player_info is not None:
        all_player_data = game_response['resultSets'][0]['rowSet']

        for player in all_player_data:
            if player_info in player:
                return player
    return game_response

def give_player_games_of_past_week(team, player_info):
    """Given some team name or abbreviation, and some player_info, returns that players games from the past week
    Input: team like 'Golden State Warriors' or 'GSW', player_info like 'Stephen Curry' or 201939
    Output: PlayerStats (see above)
    """
    last_weeks_games = give_games_of_the_past_week(games=None, datetime=date.today(), team=team)
    last_weeks_game_ids = [give_game_id(game) for game in last_weeks_games]
    player_data = [player_data_from_id(id, player_info) for id in last_weeks_game_ids]
    return player_data