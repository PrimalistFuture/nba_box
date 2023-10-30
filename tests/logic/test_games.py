import pytest
from nba_api.stats.endpoints import leaguegamelog

# ______________________________give_games_tests________________________________

def give_games(year_string, season_type='Regular Season'):
    """Given a year string and a season type defaulting to Regular Season,
    returns all of the games played in that season type for that year
    Input: year string like '2022-23', season type like 'Regular Season' or 'Playoffs' or 'All-Star'
    Output: LeagueGameLog
    """
    game_log_response = leaguegamelog.LeagueGameLog(
        counter='0',
        direction='ASC',
        league_id='00',
        player_or_team_abbreviation='T',
        season=year_string,
        season_type_all_star=season_type,
        sorter='Date'
    )

    game_logs = game_log_response.league_game_log.data['data']

    return game_logs

def test_give_games_success():
    assert len(give_games('2022-23')) == 2460
    assert len(give_games('2021-22', 'Regular Season')) == 2460
    assert len(give_games('2022-23', 'Playoffs')) == 168


# ___________________________give_games_of_this_team_tests______________________

def give_games_of_this_team(team, games=None):
    """Given team or team abbreviation and optional a set of games defaulting to those in 2023-24 if none provided, returns games from that team
    Input: team like 'Golden State Warriors' or 'GSW', games like LeagueGameLog
    Output: LeagueGameLog
    """
    if games is None:
        games = give_games('2023-24')

    teams_games = [game for game in games if team in game]
    if len(teams_games) == 0:
        return f'{team} did not play in provided games'
    else:
        return teams_games

def test_give_games_of_this_team_success():
    assert len(give_games_of_this_team('GSW', give_games('2022-23'))) == 82
    assert len(give_games_of_this_team('GSW', give_games('2022-23', 'Playoffs'))) == 13

def test_give_games_of_this_team_failure():
    assert give_games_of_this_team('STX') == 'STX did not play in provided games'


# ______________________________give_games_of_this_day_tests____________________

def give_games_of_this_day(day, games=None):
    """Given a day and a set of games defaulting to those in 2023-24 if none provided, returns games played that day
    Input: day like '2023-10-24', games like LeagueGameLog
    Output: LeagueGameLog
    """
    if games is None:
        games = give_games('2023-24')
    games_of_this_day = [game for game in games if day in game]
    if len(games_of_this_day) == 0:
        return f'No games were played on {day}'
    else:
        return games_of_this_day

def test_give_games_of_this_day_success():
    assert len(give_games_of_this_day('2023-10-24')) == 4
    assert len(give_games_of_this_day('2023-10-25')) == 24 or 34

def test_give_games_of_this_day_failure():
    assert give_games_of_this_day('2023-10-23') == 'No games were played on 2023-10-23'

# ______________________________give_game_id_tests______________________________

def give_game_id(game_log):
    """Given a single game_log, returns the game_id from that array
    Input: LeagueGameLog (see above)
    Output: '0022201230'
    """

    if len(game_log) == 29:
        game_id = game_log[4]
        return game_id
    else:
        return f'Provided game_log is probably not a valid LeagueGameLog, which must have a length of 29.'

def give_game_id_success():
    assert give_game_id([0,0,0,0,'0022201230',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) == '0022201230'

def give_game_id_failure():
    assert give_game_id([]) == 'Provided game_log is probably not a valid LeagueGameLog, which must have a length of 29.'