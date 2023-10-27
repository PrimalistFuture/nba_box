from nba_api.stats.endpoints import boxscoretraditionalv2, leaguegamelog
from datetime import date
from dates import strip_date, populate_days_of_this_past_week

# {'LeagueGameLog':['SEASON_ID','TEAM_ID','TEAM_ABBREVIATION','TEAM_NAME','GAME_ID','GAME_DATE','MATCHUP','WL','MIN','FGM','FGA','FG_PCT','FG3M','FG3A','FG3_PCT','FTM','FTA','FT_PCT','OREB','DREB','REB','AST','STL','BLK','TOV','PF','PTS','PLUS_MINUS','VIDEO_AVAILABLE']}

def give_games(year_string, season_type='Regular Season'):
    """Given a year string and a season type defaulting to Regular Season, returns all of the games played in that season type for that year
    Input: year string like '2022-23', season type like 'Regular Season' or 'Playoffs' or 'All-Star'
    Output: LeagueGameLog
    """
    game_log_response = leaguegamelog.LeagueGameLog(counter='0', direction='ASC', league_id='00', player_or_team_abbreviation='T', season=year_string, season_type_all_star=season_type, sorter='Date')

    game_logs = game_log_response.league_game_log.data['data']

    return game_logs


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


def give_games_of_this_day_for_this_team(day, team, games=None):
    """Combines two different functions to take in a day, a team and optionally some games defaulting to 2023-24, and returns all games played by that team on that day
    Input: day like '2023-10-24', team like 'Golden State Warriors' or 'GSW',games like LeagueGameLog
    Output: LeagueGameLog
    """
    if games is None:
        games = give_games('2023-24')

    games_of_this_day = give_games_of_this_day(day, games)
    games_filtered_by_date_and_team = give_games_of_this_team(team, games_of_this_day)
    return games_filtered_by_date_and_team


def give_games_of_the_past_week(games=None, datetime=date.today(), team=None):
    """Given comprehensed game_log data list, a datetime_dict and an optional team or team abbreviation, return all of the games played, optionally by that team, in the past week
    Input: game data list, datetime like datetime.date(2023,10,20), team like 'Golden State Warriors' or 'GSW'
    Output: game data list"""
    if games is None:
        games = give_games('2023-24')

    days_of_past_week = populate_days_of_this_past_week(datetime)

    games_of_past_week = [game for game in games for day in days_of_past_week if day in game]

    if team is not None:
        teams_games = give_games_of_this_team(team, games_of_past_week)
        return teams_games
    return games_of_past_week


def give_game_id(game_log):
    """Given a single game_log_array, returns the game_id from that array
    Input: LeagueGameLog (see above)
    Output: '0022201230'
    """
    game_id = game_log[4]
    return game_id

