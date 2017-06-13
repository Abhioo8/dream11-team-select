#!/home/lokesh/.virtualenvs/python2.7/bin/python2.7
from flask import Flask,jsonify,render_template
from get_player_odds import read_from_players

app = Flask(__name__)

@app.route('/players/list', methods=['GET'])
def index():
    ordered_players = read_from_players()
    return jsonify({'players':ordered_players})

@app.route('/')
def _main():
    players_dict = read_from_players()
    return render_template('index.html', players_bat_dict=players_dict['BAT'],
    			players_wk_dict=players_dict['WK'], 
    			players_bowl_dict=players_dict['BOWL'], 
    			players_ar_dict=players_dict['AR'],
    			total=0, teams=0)


if __name__ == '__main__':
    app.run(debug=True)