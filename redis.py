class SimpleDatabase(object):

	def __init__(self):
		self.transactions = []
		self.database = {}

	def set_(self, name, value):
		if self.transactions:
			if name in self.database and name not in self.transactions[0]:
				self.transactions[0][name] = self.database[name]
			if name not in self.database:
				self.transactions[0][name] = None
		self.write(name, value)

	def get(self, name):
		if name in self.database:
			return str(self.database[name])
		else:
			return 'NULL'

	def unset(self, name):
		if name in self.database:
			del self.database[name]

	def numequalto(self, value):
		count = 0
		for val in self.database.values():
			if val == value:
				count += 1
		return count

	def write(self, name, value):
		if value is None:
			del self.database[name]
		else:
			self.database[name] = value

	def begin(self):
		self.transactions.insert(0, {})

	def rollback(self):
		for key, val in self.transactions[0].iteritems():
			self.write(key, val)
		self.transactions.pop(0)

	def commit(self):
		self.transactions = []

def main():

	db = SimpleDatabase()
	running = True	

	while running:
		user_input = raw_input()
		commands = user_input.split(' ')

		if commands[0] == 'SET':
			db.set_(commands[1], commands[2])

		if commands[0] == 'GET':
			print db.get(commands[1])

		if commands[0] == 'UNSET':
			db.unset(commands[1])

		if commands[0] == 'NUMEQUALTO':
			print db.numequalto(commands[1])

		if commands[0] == 'END':
			running = False

		if commands[0] =='BEGIN':
			db.begin()

		if commands[0] =='ROLLBACK':
			if not db.transactions:
				print 'NO TRANSACTION'
			else:
				db.rollback()

		if commands[0] == 'COMMIT':
			db.commit()

if __name__ == '__main__':
	main()
