from flask import Flask  
from flask import render_template

import nba_py

from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():


	today_date = datetime.today()
	clean_today_date = today_date.strftime("%b %d, %Y")

	games = find_games(today_date)

	return render_template("index.html", 
					title=" Daily Scores",
					games=games,
					clean_today_date=clean_today_date)


def find_games(date):
	"""Get games for the current day.
	
	Arguments
		date: the date which we want to see the games

	This will return an array of the games that are played for that day
	"""
	scoreboard = nba_py.Scoreboard(month=date.month,
									day=date.day,
									year=date.year)

	line_score = scoreboard.line_score()

	# the total list of games
	games = []

	#current game currently looked at
	current_game = {}

	current_game_sequence = 0
	counter_game = 0

	for teams in line_score:
		if(teams["GAME_SEQUENCE"] != current_game_sequence):
			current_game["TEAM_1_ABBREVIATION"] = teams["TEAM_ABBREVIATION"]
			current_game["TEAM_1_WINS_LOSSES"] = teams["TEAM_WINS_LOSSES"]

			current_game["TEAM_1_PTS"] = teams["PTS"]
			current_game["TEAM_1_ID"] = teams["TEAM_ID"]

			current_game_sequence = teams["GAME_SEQUENCE"]
			counter_game += 1
		elif (counter_game == 1):
			current_game["TEAM_2_ABBREVIATION"] = teams["TEAM_ABBREVIATION"]
			current_game["TEAM_2_WINS_LOSSES"] = teams["TEAM_WINS_LOSSES"]

			current_game["TEAM_2_PTS"] = teams["PTS"]
			current_game["TEAM_2_ID"] = teams["TEAM_ID"]

			current_game["GAME_ID"] = teams["GAME_ID"]

			games.append(current_game)

			current_game = {}
			counter_game = 0

	return games



if __name__=="__main__":
	# app.run(threaded = true)
	app.run(host="127.0.0.1", port=8080,threaded=True, debug =True)
