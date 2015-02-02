import copy

def set_(commands, redis_dictionary, reverse_dictionary, stack):
	if (commands[1] in redis_dictionary) and (stack == []):
		reverse_dictionary[redis_dictionary[commands[1]]].remove(commands[1])
		if reverse_dictionary[redis_dictionary[commands[1]]] == []:
			del reverse_dictionary[redis_dictionary[commands[1]]]
	dict[commands[1]] = commands[2]
	if commands[2] not in reverse_dictionary:
		reverse_dictionary[commands[2]] = [commands[1]]
	else:
		reverse_dictionary[commands[2]].append(commands[1])

def get(commands, redis_dictionary):
	if commands[1] in redis_dictionary:
		print str(redis_dictionary[commands[1]]) 
	else:
		print 'NULL'

def unset(commands, redis_dictionary, reverse_dictionary):
	reverse_dictionary[redis_dictionary[commands[1]]].remove(commands[1])
	del redis_dictionary[commands[1]]

def numequalto(commands, reverse_dictionary):
	if commands[1] in reverse_dictionary:
		print str(len(reverse_dictionary[commands[1]]))
	else:
		print '0'

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
		commands = user_input.split(' ')
		if commands[0] == 'SET':
			if stack == []:
				set_(commands, redis_dictionary, reverse_dictionary, stack)
			else:
				set_(commands, stack[-1][0], stack[-1][1], stack)
		if commands[0] == 'GET':
			if stack == []:
				get(commands, redis_dictionary)
			else:
				get(commands, stack[-1][0])
		if commands[0] == 'UNSET':
			if stack == []:
				unset(commands, redis_dictionary, reverse_dictionary)
			else:
				unset(commands, stack[-1][0], stack[-1][1])
		if commands[0] == 'NUMEQUALTO':
			if stack == []:
				numequalto(commands, reverse_dictionary)
			else:
				numequalto(commands, stack[-1][1])
		if commands[0] == 'END':
			running = False
		if commands[0] =='BEGIN':
			begin(redis_dictionary, reverse_dictionary, stack)
		if commands[0] =='ROLLBACK':
			rollback(stack)
		if commands[0] == 'COMMIT':
			redis_dictionary = stack[-1][0]
			reverse_dictionary = stack[-1][0]
			stack = []

if __name__ == '__main__':
	main()
