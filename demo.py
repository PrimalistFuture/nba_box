import os
import inspect
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
career = playercareerstats.PlayerCareerStats(player_id='203999')

# pandas data frames (optional: pip install pandas)
career.get_data_frames()[0]

# json
career.get_json()

# dictionary
career.get_dict()


# ---------------- TEAMS TEST -------------------------

# get_teams returns a list of 30 dictionaries, each an NBA team.
nba_teams = teams.get_teams()
print("Number of teams fetched: {}".format(len(nba_teams)))
nba_teams[:3]

nba_players = players.get_players()
print("Number of players fetched: {}".format(len(nba_players)))
nba_players[:5]

# To search for an individual team or player by its name (or other attribute), dictionary comprehensions are your friend.
warriors = [team for team in nba_teams if team["full_name"] == "Golden State Warriors"][0]

# ---------------- PLAYER TEST -------------------------

human_torch = [player for player in nba_players if player["full_name"] == "Stephen Curry"]

# ---------------- BOXSCORESCORING TEST ------------------------

game_scoring = boxscorescoringv2.BoxScoreScoringV2(game_id="0021700807")

# pandas data frames (optional: pip install pandas)
game_scoring.get_data_frames()[0]

# json
game_scoring.get_json()

# dictionary
game_scoring.get_dict()

# ---------------- BOXSCORETRADITIONAL TEST ------------------------

game_traditional = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id="0021700807")

# ---------------- LEAGUESTANDINGS TEST ------------------------

standings = leaguestandingsv3.LeagueStandingsV3(league_id="00", season="2022-23", season_type="Regular Season")

# This seems to be exactly what I want
game_scoring.get_data_frames()

# ---------------- LEAGUEGAMELOG TEST ------------------------

# Seems to give absolutely every game from this season. I need a way for it to give me the games from the last few days. There might be a better end
game_log = leaguegamelog.LeagueGameLog(counter='0', direction='ASC', league_id='00', player_or_team_abbreviation='T', season='2022-23', season_type_all_star='Regular Season', sorter='Date')

# date_to_nullable='2022-08-15', date_from_nullable='2022-08-22'

