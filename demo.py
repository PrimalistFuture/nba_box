import os

from flask import Flask
# from flask_debugtoolbar import DebugToolbarExtension
from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import playercareerstats

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


# ___________

# get_teams returns a list of 30 dictionaries, each an NBA team.
nba_teams = teams.get_teams()
print("Number of teams fetched: {}".format(len(nba_teams)))
nba_teams[:3]

nba_players = players.get_players()
print("Number of players fetched: {}".format(len(nba_players)))
nba_players[:5]

# To search for an individual team or player by its name (or other attribute), dictionary comprehensions are your friend.
warriors = [team for team in nba_teams if team["full_name"] == "Golden State Warriors"][0]

human_torch = [player for player in nba_players if player["full_name"] == "Stephen Curry"]