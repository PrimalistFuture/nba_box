import pytest
from nba_api.stats.endpoints import boxscoretraditionalv2

# ____________________player_data_from_id_tests_________________________________

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

def test_player_data_from_id_success():
    assert len(player_data_from_id('0022201230')) == 3
    assert 'Stephen Curry' in player_data_from_id('0022201230', 'Stephen Curry')
    assert 'Stephen Curry' in player_data_from_id('0022201230', 201939)

def test_player_data_from_id_failure():
    assert player_data_from_id(1022201230) == '1022201230 must be a string.'
    assert player_data_from_id('022201230') == '022201230 is not a valid game_id. Ensure the the game_id has a length of 10.'