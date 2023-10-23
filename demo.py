import os
from datetime import date, timedelta
from flask import Flask
# from flask_debugtoolbar import DebugToolbarExtension
from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import playercareerstats, boxscorescoringv2, boxscoretraditionalv2, leaguestandingsv3, leaguegamelog

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///sts_test')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


# Nikola Jokić
# career = playercareerstats.PlayerCareerStats(player_id='203999')

# pandas data frames (optional: pip install pandas)
# career.get_data_frames()[0]

# json
# career.get_json()

# dictionary
# career.get_dict()


# ---------------- TEAMS TEST -------------------------

# get_teams returns a list of 30 dictionaries, each an NBA team.
# nba_teams = teams.get_teams()
# print("Number of teams fetched: {}".format(len(nba_teams)))
# nba_teams[:3]

# To search for an individual team or player by its name (or other attribute), dictionary comprehensions are your friend.
# warriors = [team for team in nba_teams if team["full_name"] == "Golden State Warriors"][0]


# ---------------- PLAYER TEST -------------------------

# nba_players = players.get_players()
# print("Number of players fetched: {}".format(len(nba_players)))
# nba_players[:5]

# To search for an individual team or player by its name (or other attribute), dictionary comprehensions are your friend.

# human_torch = [player for player in nba_players if player["full_name"] == "Stephen Curry"]

# ---------------- BOXSCORESCORING TEST ------------------------

# game_scoring = boxscorescoringv2.BoxScoreScoringV2(game_id="0021700807")

# pandas data frames (optional: pip install pandas)
# game_scoring.get_data_frames()[0]

# json
# game_scoring.get_json()

# dictionary
# game_scoring.get_dict()

# This seems to be exactly what I want
# game_scoring.get_data_frames()

# ---------------- BOXSCORETRADITIONAL TEST ------------------------

# game_traditional = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id="0021700807")

# ---------------- LEAGUESTANDINGS TEST ------------------------

# standings = leaguestandingsv3.LeagueStandingsV3(league_id="00", season="2022-23", season_type="Regular Season")

# ---------------- LEAGUEGAMELOG TEST ------------------------

# Seems to give absolutely every game from this season. I need a way for it to give me the games from the last few days. There might be a better endpoint
game_log = leaguegamelog.LeagueGameLog(counter='0', direction='ASC', league_id='00', player_or_team_abbreviation='T', season='2022-23', season_type_all_star='Regular Season', sorter='Date')


game_log.expected_data
# ['SEASON_ID',
#   'TEAM_ID',
#   'TEAM_ABBREVIATION',
#   'TEAM_NAME',
#   'GAME_ID',
#   'GAME_DATE',
#   'MATCHUP',
#   'WL',
#   'MIN',
#   'FGM',
#   'FGA',
#   'FG_PCT',
#   'FG3M',
#   'FG3A',
#   'FG3_PCT',
#   'FTM',
#   'FTA',
#   'FT_PCT',
#   'OREB',
#   'DREB',
#   'REB',
#   'AST',
#   'STL',
#   'BLK',
#   'TOV',
#   'PF',
#   'PTS',
#   'PLUS_MINUS',
#   'VIDEO_AVAILABLE']


# This is what I am pretty sure are the right arguments for this leaguegamelog, but I am not sure if this is the date format they want.
# date_to_nullable='2022-11-22', date_from_nullable='2022-11-15'

# last_weeks_games = [game for game in game_log if game['GAME_DATE'] == '2022-11-15']

# this is the bit that confuses me: when I had the same thing but with .data instead, it didn't work so I sort of thought it didn't exist in the shape I thought it did.
games = game_log.league_game_log.data['data']

# day = '2023-04-09'

# team = 'GSW'
# team2 = 'POR'

# Holy shit I did it. I have shown that I can grab just games from a specific day
# Lets try the same thing but for just a specific team
def give_games_of_this_day_for_this_team(games, day, team=None):
    """Takes in the comprehensed game_log data, and given a day and an optional team, prints the game_log data from those specifications."""
    games_of_this_day = [game for game in games if day in game]
    if team is not None:
        games_filtered_by_date_and_team = give_games_of_this_team(games_of_this_day, team)
        if len(games_filtered_by_date_and_team) == 0:
            print(f'{team} did not play on {day}')
        else:
            return games_filtered_by_date_and_team
    if len(games_of_this_day) == 0:
        print(f'No games were played on {day}')
    else:
        return games_of_this_day

def give_games_of_this_team(games, team):
    """Helper func that takes in games and a team, and returns games from that team"""
    teams_games = [game for game in games if team in game]
    return teams_games


# ---------------- DATETIME DATE TODAY TEST ------------------------

today = date.today()
# 2023, 10, 20
week = timedelta(days=7)
# I can't just plug in a 7 below, it wants it like this
start_of_last_week = today - week
# 2023, 10, 13
start_of_last_week.year
# 2023
start_of_last_week.month
# 10
start_of_last_week.day
# 13

# date doesn't give accept or return leading 0s, which the nba stats expect.
april_9_2023 = date(2023, 4, 9)
# datetime.date(2022, 4, 9)

# I think in a perfect world, I would want to add the leading 0s later, but its gotta happen at some point.
def strip_date(datetime_dict):
    """Given datetime obj, returns string of year-month-day
    Input = datetime_dict like datetime.date(2023,10,13)
    Output = '2023-10-13'
    """
    singles = [1,2,3,4,5,6,7,8,9]

    year = datetime_dict.year

    month = datetime_dict.month
    if month in singles:
        month = f'0{month}'

    day = datetime_dict.day
    if day in singles:
        day = f'0{day}'

    return f'{year}-{month}-{day}'

# Now I think I need functions that will give the datetime objects for each day between today and last week
# There has to be someway to do this dynamically, but I can't think of it

def populate_days_of_this_past_week(today_datetime):
    """Given a datetime obj, returns an array of stringed dates from the past week
    Input: datetime_dict like datetime.date(2023,10,20)
    Output: ['2023-10-20', '2023-10-19', ... '2023-10-13']"""
    one_day = timedelta(days=1)
    two_day = timedelta(days=2)
    three_day = timedelta(days=3)
    four_day = timedelta(days=4)
    five_day = timedelta(days=5)
    six_day = timedelta(days=6)
    seven_day = timedelta(days=7)
    days = [one_day, two_day, three_day, four_day, five_day, six_day, seven_day]

    all_days_of_this_past_week = [strip_date(today_datetime - day) for day in days]
    return all_days_of_this_past_week




# ---------------- Putting it all together ------------------------


# Now I need to go into the giant game_log data and just get the games from this past week and from a given team.

def give_games_of_the_past_week(games, datetime, team=None):
    """Given comprehensed game_log data list, a datetime_dict and an optional team or team abbreviation, return all of the games played, optionally by that team, in the past week
    Input: game data list, datetime_dict like datetime.date(2023,10,20), team like 'Golden State Warriors' or 'GSW'
    Output: game data list"""
    days_of_past_week = populate_days_of_this_past_week(datetime)
    # ['2023-10-22', '2023-10-21', ..., '2023-10-16']

    # pretty cool nested for loop in a comprehension. Below is the uncool way but far more readable
    games_of_past_week = [game for game in games for day in days_of_past_week if day in game]
    # games_of_past_week = []
    # for game in games:
    #     for day in days_of_past_week:
    #         if day in game:
    #             # print(game)
    #             games_of_past_week.append(game)
    if team is not None:
        teams_games = give_games_of_this_team(games_of_past_week, team)
        return teams_games
    return games_of_past_week


