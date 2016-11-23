'''
Team menbers: Fei Zhao (fzs347), Yimin Chen (yci057)
'''
import copy

def check_win(board):
	threes = ((1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(1,5,9),(3,5,7))
	for each in threes:
		total = board[each[0]-1] + board[each[1]-1] + board[each[2]-1]
		if total == -3:
			return "O"
		elif total == 3:
			return "X"
	return "No Winner"

def find_valid_move(board):
	valid_moves = []
	i = 0
	for position in board:
		if position == 0:
			valid_moves.append(i)
		i = i + 1
	return valid_moves # 0 - 8

def find_cur_player(board):
	o = 0
	x = 0
	for target in board:
		if target == -1:
			o += 1
		elif target == 1:
			x += 1
	if o == x:
		return 'X'
	else:
		return 'O'

def cal_values(board, mysymbol): # mysymbol will always be ai's symbol, minmax
	cur_symbol = find_cur_player(board)
	if cur_symbol == 'X':
		target = 1
	else:
		target = -1

	children_values = []

	winner = check_win(board)
	if winner == mysymbol:
		return 10
	elif winner == "No Winner":
		if 0 in board:
			valid_moves = find_valid_move(board)
			for position in valid_moves:
				temp_board = copy.deepcopy(board)
				temp_board[position] = target
				children_values.append(cal_values(temp_board, mysymbol))
			if cur_symbol == mysymbol:
				return max(children_values)
			else:
				return min(children_values)
		else:
			return 0
	else:
		return -10

def cal_values_abpruning(board, mysymbol): # mysymbol will always be ai's symbol, minmax, a/b pruning
	cur_symbol = find_cur_player(board)
	if cur_symbol == 'X':
		target = 1
	else:
		target = -1

	children_values = []

	winner = check_win(board)
	if winner == mysymbol:
		return 10
	elif winner == "No Winner":
		if 0 in board:
			valid_moves = find_valid_move(board)
			for position in valid_moves:
				if 10 in children_values and cur_symbol == mysymbol:
					return 10
				if -10 in children_values and cur_symbol != mysymbol:
					return -10
				temp_board = copy.deepcopy(board)
				temp_board[position] = target
				children_values.append(cal_values_abpruning(temp_board, mysymbol))
			if cur_symbol == mysymbol:
				return max(children_values)
			else:
				return min(children_values)
		else:
			return 0
	else:
		return -10

def mymove(board, mysymbol):
	print "Board as seen by the machine:",
	print board
	print "The machine is playing:",
	print mysymbol

	if mysymbol == 'X':
		target = 1
	else:
		target = -1

	move_values = {}
	valid_moves = find_valid_move(board)
	for position in valid_moves:
		temp_board = copy.deepcopy(board)
		temp_board[position] = target
		#move_values[position] = cal_values(temp_board, mysymbol)
		move_values[position] = cal_values_abpruning(temp_board, mysymbol)
	max_value = max(move_values.values())
	for move in move_values:
		if move_values[move] == max_value:
			best_move = move
			break
	return best_move + 1
