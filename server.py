from flask import Flask
from flask import request
from flask_cors import CORS
import json
from character import Character
from messages import messages


app = Flask(__name__)
CORS(app)

game_instances = {}


# When a user lands on the page, the welcome message is sent
@app.route('/start', methods=["POST"])
def handle_start():
    data_set = {'output': messages["welcome"]}
    json_dump = json.dumps(data_set)
    return json_dump


# When a new game is started, create a game instance and store it in the dict
# return the current room and intro message
@app.route('/new', methods=["POST"])
def handle_new_game():
    port = str(request.environ.get('REMOTE_PORT'))
    player = Character('Marni')
    game_instances[port] = player
    intro = game_instances[port].newgame(port)
    data_set = {'output': intro,
                'location': game_instances[port].location.room_name}
    json_dump = json.dumps(data_set)
    return json_dump


# When a user sends a command, 
@app.route('/', methods=["GET", "POST"])
def handle_interaction():
    port = str(request.environ.get('REMOTE_PORT'))
    player = game_instances[port]
    command = str(request.args.get('command'))
    output = player.handle_user_input(command)
    data_set = {'output': output, 'location': player.location.room_name}
    json_dump = json.dumps(data_set)
    return json_dump


@app.route('/quit', methods=["POST"])
def handle_quit_game():
    port = str(request.environ.get('REMOTE_PORT'))
    player = game_instances[port]
    data_set = {'output': 'Game Over',
                'location': player.location.room_name}
    json_dump = json.dumps(data_set)
    del game_instances[port]
    return json_dump


@app.route('/save', methods=["POST"])
def handle_save():
    port = str(request.environ.get('REMOTE_PORT'))
    player = game_instances[port]
    # output = player.savegame()
    data_set = {'output': 'Game Progress Saved',
                'location': player.location.room_name}
    json_dump = json.dumps(data_set)
    return json_dump


@app.route('/load', methods=["GET"])
def handle_load():
    port = str(request.environ.get('REMOTE_PORT'))
    player = game_instances[port]
    # output = player.loadgame()
    data_set = {'output': 'Game Loaded from Last Save',
                'location': player.location.room_name}
    json_dump = json.dumps(data_set)
    return json_dump


if __name__ == '__main__':
    app.run_server(debug=False)
