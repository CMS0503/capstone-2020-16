import os
import sys
import json
import requests

from gamemanager import GameManager
from userprogram import UserProgram


def match(data):
    match_data = data
    match_dir = os.getcwd()  # os.path.join(os.getcwd(), 'match')
    extension = {'': '', 'C': '.c', 'C++': '.cpp', 'PYTHON': '.py', 'JAVA': '.java'}
    update_url = 'http://203.246.112.32:8000/api/v1/game/' + str(match_data['match_id']) + '/'

    challenger_code_filename = 'challenger{0}'.format(extension[match_data['challenger_language']])
    oppositer_code_filename = 'oppositer{0}'.format(extension[match_data['opposite_language']])

    challenger_code_path = os.path.join(match_dir, challenger_code_filename)
    oppositer_code_path = os.path.join(match_dir, oppositer_code_filename)

    challenger_code = match_data['challenger_code']
    oppositer_code = match_data['opposite_code']

    with open(challenger_code_path, 'w') as f:
        f.write(challenger_code)

    with open(oppositer_code_path, 'w') as f:
        f.write(oppositer_code)

    challenger = UserProgram('challenger', match_data['challenger'], match_data['challenger_language'], match_dir,
                             challenger_code_filename)
    oppositer = UserProgram('opposite', match_data['opposite'], match_data['opposite_language'], match_dir,
                            oppositer_code_filename)

    game_manager = GameManager(challenger=challenger, oppositer=oppositer,
                               placement_rule=match_data['placement'], action_rule=match_data['action'],
                               ending_rule=match_data['ending'],
                               board_size=match_data['board_size'], board_info=match_data['board_info'],
                               obj_num=match_data['obj_num'], problem=match_data['problem'])

    winner, board_record, placement_record, result, error_msg = game_manager.play_game()
    # with open('result.txt', 'w') as f:
    #    f.write(match_result)
    # with open('result.txt', 'a') as f:
    #    f.write(board_record)
    # with open('result.txt', 'a') as f:
    #    f.write(placement_record)
    data = {"winner": winner, "record": board_record, "placement_record": placement_record, "result": result,
            "error_msg": error_msg}
    data2 = {"winner": winner, "placement_record": placement_record, "result": result,
            "error_msg": error_msg}
    print(data2)
    r = requests.patch(update_url, data=data)
    print('request ok')


if __name__ == '__main__':
    # json_data = json.loads(sys.argv[1])

    with open('matchdata.json') as json_file:
        json_data = json.load(json_file)
    match(json_data)



