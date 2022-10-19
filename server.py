from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import json
# from main import test_function
from character import Character
from main import check_and_move, init_room_list_and_items

app = Flask(__name__)
CORS(app)

room_list = init_room_list_and_items()
player = Character("Player 1", location=room_list[0])


@app.route('/', methods=["GET", "POST"])
@cross_origin(origin='*', headers=['Content-Type', 'application/json'])
def handle_request():
    command = str(request.args.get('command'))
    output = check_and_move(command, player.location, room_list)
    player.set_location(output)
    # output = test_function(command)
    data_set = {'output': output}
    json_dump = json.dumps(data_set)
    return json_dump


if __name__ == '__main__':
    app.run_server(debug=False)
