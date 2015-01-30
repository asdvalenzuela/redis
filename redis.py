import copy

def set_(command_list, dict, reverse_dict, stack):
	if (command_list[1] in dict) and (stack == []):
		reverse_dict[dict[command_list[1]]].remove(command_list[1])
		if reverse_dict[dict[command_list[1]]] == []:
			del reverse_dict[dict[command_list[1]]]
	dict[command_list[1]] = command_list[2]
	if command_list[2] not in reverse_dict:
		reverse_dict[command_list[2]] = [command_list[1]]
	else:
		reverse_dict[command_list[2]].append(command_list[1])

def get(command_list, dict):
	if command_list[1] in dict:
		print str(dict[command_list[1]]) 
	else:
		print "NULL"

def unset(command_list, dict, reverse_dict):
	reverse_dict[dict[command_list[1]]].remove(command_list[1])
	del dict[command_list[1]]

def numequalto(command_list, reverse_dict):
	if command_list[1] in reverse_dict:
		print str(len(reverse_dict[command_list[1]]))
	else:
		print "0"

def begin(redis_dictionary, reverse_dictionary, stack):
	temp_redis_dict = copy.deepcopy(redis_dictionary)
	temp_reverse_dict = copy.deepcopy(reverse_dictionary)
	stack.append((temp_redis_dict, temp_reverse_dict))

def rollback(stack):
	if len(stack) > 0:
		stack.pop()
	else:
		print 'NO TRANSACTION'

def main():

	redis_dictionary = {}
	reverse_dictionary = {}
	stack = []
	running = True	

	while running:
		user_input = raw_input()
		command_list = user_input.split(" ")
		if command_list[0] == 'SET':
			if stack == []:
				set_(command_list, redis_dictionary, reverse_dictionary, stack)
			else:
				set_(command_list, stack[-1][0], stack[-1][1], stack)
		if command_list[0] == 'GET':
			if stack == []:
				get(command_list, redis_dictionary)
			else:
				get(command_list, stack[-1][0])
		if command_list[0] == 'UNSET':
			if stack == []:
				unset(command_list, redis_dictionary, reverse_dictionary)
			else:
				unset(command_list, stack[-1][0], stack[-1][1])
		if command_list[0] == 'NUMEQUALTO':
			if stack == []:
				numequalto(command_list, reverse_dictionary)
			else:
				numequalto(command_list, stack[-1][1])
		if command_list[0] == 'END':
			running = False
		if command_list[0] =='BEGIN':
			begin(redis_dictionary, reverse_dictionary, stack)
		if command_list[0] =='ROLLBACK':
			rollback(stack)
		if command_list[0] == 'COMMIT':
			redis_dictionary = stack[-1][0]
			reverse_dictionary = stack[-1][0]
			stack = []

if __name__ == "__main__":
	main()
