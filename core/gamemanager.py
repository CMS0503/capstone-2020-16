import numpy as np
import os
import re
import sys
import time

from placement_rule import PlacementRule
from action_rule import ActionRule
from ending_rule import EndingRule
from game_data import GameData
from execute_code import Execution


def test():
    print('test')


class GameManager:
    def __init__(self, challenger, oppositer, placement_rule, action_rule, ending_rule, board_size, board_info, obj_num, problem):
        self.board = np.zeros((board_size, board_size), dtype='i')
        self.board_info = board_info
        self.board_size = board_size
        self.board_record = ''

        # self.board = board_info
        self.check_turn = 'challenger'
        self.challenger = challenger
        self.opposite = oppositer

        self.game_data = GameData(placement_rule, action_rule, ending_rule, board_size, board_info, obj_num, problem)
        self.placement_rule = PlacementRule()
        self.action_rule = ActionRule()
        self.ending_rule = EndingRule()

        self.execution = Execution()

        self.placement_record = ''

        self.limit_time = 2000

        self.error_msg = None

    def play_game(self):
        print('## Start Game ##')
        total_turn = 0
        total_turn_limit = 100 # self.game_data.board_size ** 3
        is_ending = False
        match_result = ''
        winner = 0
        output = None

        self.board_record += str(self.board_info) + ' \n'
        self.board = self.parsing_board_info(self.board_info, self.board_size)
        self.compile_user_code()

        while not is_ending:
            print('######')
            if total_turn > total_turn_limit:
                print("total_turn over")
                self.error_msg = 'total turn over'
                match_result = 'draw'
                return match_result

            self.make_board_data()

            ## Execute user code
            output = None
            print('Execute user program...', end='')
            try:
                if os.path.isfile("placement.txt"):
                    os.remove("placement.txt")
                    # print('delete placement.txt')
                if self.check_turn == 'challenger':
                    output = self.execution.execute_program(self.challenger.play(), self.challenger.save_path)
                elif self.check_turn == 'opposite':
                    output = self.execution.execute_program(self.opposite.play(), self.opposite.save_path)
            except Exception as e:
                self.error_msg = e
                # print(self.error_msg)
                break
            print('OK')
            print('Output :', output, end='')

            print('Turn :', self.check_turn)
            print(self.board)

            ## Start check rule

            # Check Placement Rule
            print('Check placement rule...', end='')
            try:
                check_placement, new_board = self.placement_rule.check_placement_rule(self.game_data, self.board, output)
            except Exception as e:
                self.error_msg = f'Error in check placement rule : {e}'
                # print(self.error_msg)
                break
            print(check_placement)

            # Check Action Rule
            self.board = new_board
            print('Check action rule...', end='')
            try:
                apply_action, new_board = self.action_rule.apply_action_rule(self.game_data, self.board, output)
            except Exception as e:
                self.error_msg = f'Error in check action rule : {e}'
                # print(self.error_msg)
                break
            print(apply_action)

            # Check Ending Rule
            self.board = new_board
            print('Check ending rule...', end='')
            try:
                is_ending, winner = self.ending_rule.check_ending(self.game_data, self.board, output) # ending_result = self.ending_rule.check_ending(self.game_data, self.board, output)
            except Exception as e:
                self.error_msg = f'Error check ending rule : {e}'
                # print(self.error_msg, '\n')
                break
            print(is_ending, '\n')

            self.add_record(output)

            # End game
            if is_ending is True:
                print('End Game')
                if winner == 1:
                    winner = self.check_turn
                elif winner == -1:
                    if self.check_turn == 'challenger':
                        winner = 'opposite'
                    else:
                        winner = 'challenger'
                else:
                    winner = 'draw'
                match_result = 'finish'
                self.error_msg = 'no error'

            # change turn
            elif is_ending is False:
                total_turn += 1
                self.check_turn = 'challenger' if self.check_turn == 'opposite' else 'opposite'

        # End game with error
        if self.error_msg != 'no error':
            print('End with error')
            if self.check_turn == 'challenger':
                winner = 'opposite'
                match_result = 'challenger_error'
            else:
                winner = 'challenger'
                match_result = 'opposite_error'

            if output == '':
                print('no output')
                if self.error_msg != 'Time Over':
                    self.error_msg = 'RunTimeError' 

            else:
                self.error_msg = str(self.error_msg) + f'--> placement = {output}'
        
        print(self.error_msg)
        # print('winner', winner)

        return winner, self.board_record, self.placement_record, match_result, self.error_msg

    def play_with_me(self, placement):
        print('Start Play With Me')
        # self.board_record += str(self.board_info) + ' \n'
        self.board = self.parsing_board_info(self.board_info, self.board_size)
        self.compile_user_code()

        is_ending = False

        placement_code = None
        match_result = 'not finish'
        print('Start Check Rule...')
        for i in range(2):
            print('\n' + '#######')
            self.make_board_data()

            output = None
            if i == 0:
                print('Receive Borad')
                print(self.board)

            ## Execute user code
            
            if i == 1:  # only code turn
                try:
                    print('Execute user program...', end='')
                    if os.path.isfile("placement.txt"):
                        os.remove("placement.txt")
                    output = self.execution.execute_program(self.challenger.play(), self.challenger.save_path)
                    placement_code = output
                except Exception as e:
                    self.error_msg = f'Program error in execute user program : {e}'
                    print(self.error_msg)
                    break
            else:
                print('User placement:', placement,'...', end='')
                output = placement
            print('OK', output)
            ## Start Check Rule

            # Check Placement Rule
            print('Check Placement Rule...', end='')
            try:
                check_placement, new_board = self.placement_rule.check_placement_rule(self.game_data, self.board, output)
            except Exception as e:
                self.error_msg = f'placement error : {e}'
                print(self.error_msg)
                break
            print(check_placement)

            # After placement board
            self.board = new_board

            # Check Action Rule
            print('Check action rule...', end='')
            try:
                apply_action, new_board = self.action_rule.apply_action_rule(self.game_data, self.board, output)
            except Exception as e:
                self.error_msg = f'action error : {e}'
                print(self.error_msg)
                break
            print(apply_action, new_board)

            # After action board
            self.board = new_board

            # Check Ending Rule
            print('Check ending rule...', end='')
            try:
                is_ending, winner = self.ending_rule.check_ending(self.game_data, self.board, output)
            except Exception as e:
                print('errrrrrrrrror')
                self.error_msg = f'ending error : {e}'
                print(self.error_msg)
                break
            print(is_ending, '\n')

            if i == 0:
                print('# After user action board')
                print(self.board)
                self.add_data(self.board, output) 

            else:
                self.add_data(self.board*(-1), output)
                print('# After Code action board')
                print(self.board * (-1))

            # End game
            if is_ending is True:
                print('End Game', winner)
                if winner == 1:
                    winner = self.check_turn
                elif winner == -1:
                    if self.check_turn == 'challenger':
                        winner = 'opposite'
                    else:
                        winner = 'challenger'
                else:
                    winner = 'draw'
                match_result = 'finish'
                self.error_msg = 'no error'
                if winner == 'challenger':
                    self.add_data(self.board, output)
                break

            elif is_ending is False:
                self.check_turn = 'challenger' if self.check_turn == 'opposite' else 'opposite'
                self.board *= -1
        # End game with error
        if self.error_msg != 'no error' and self.error_msg is not None:
            print('End error', str(self.error_msg))
            if self.check_turn == 'challenger':
                winner = 'opposite'
                match_result = 'challenger_error'
            else:
                winner = 'challenger'
                match_result = 'opposite_error'

            if output is not None:
                self.error_msg = str(self.error_msg) + f'--> placement = {output}'

        print('winner', winner)
        print(self.board_record)
        return match_result, winner, self.board_record, placement_code

    def compile_user_code(self):
        try:
            self.execution.execute_program(self.challenger.compile(), self.challenger.save_path)
        except KeyError as e:
            return False

        try:
            self.execution.execute_program(self.opposite.compile(), self.opposite.save_path)
        except KeyError as e:
            return False
        print('compile')
        return True

    def add_data(self, board, output):
        self.placement_record += str(output).strip() + '\n'

        for line in board:
            for i in line:
                self.board_record += (str(i) + ' ')

        self.board_record += '\n'

    def make_board_data(self):
        with open(os.path.join(self.challenger.save_path, 'board.txt'), 'w') as f:
            temp = ''
            for line in self.board:
                for i in line:
                    temp += (str(i) + ' ')
                temp += '\n'
            f.write(temp)

    def add_record(self, output):
        if self.check_turn == 'challenger':
            self.add_data(self.board, output)
            self.board *= -1

        else:
            self.board *= -1
            self.add_data(self.board, output)

    def parsing_user_output(self, output):
        placement = []
        if '>' in output:
            pass
        else:
            placement = [int(i) for i in output.split()]

        return placement

    def parsing_board_info(self, board_info, board_size):
        numbers = board_info.split()
        board = np.zeros((board_size, board_size), dtype='i')
        for i in range(board_size):
            for j in range(board_size):
                board[i][j] = int(numbers[i*board_size + j])

        return board
