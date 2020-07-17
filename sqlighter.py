import sqlite3, random

class SQLighter:

	def __init__(self, database):
		"""Подключаемся к БД и сохраняем курсор соединения"""
		self.connection = sqlite3.connect(database)
		self.cursor = self.connection.cursor()

	def add_db(self, user_id, user_name):
		code = ''
		i = random.randint(-10, 10)
		if i > 3:
			code += 'T'
		elif i == 3:
			code += 'F'
		else:
			code += 'W'
		code += str(user_id)[len(str(user_id))- 3]
		i = random.randint(-10, 10)
		if i < 0:
			code += 'R'
		else:
			code += 'P'
		code += '-'
		i = random.randint(-10, 10)
		if i > 0:
			code += 'Y'
		else:
			code += '3'
		code += str(user_id)[len(str(user_id))-2]
		i = random.randint(-10, 10)
		if i > 5:
			code += 'I'
		else:
			code += 'Q'
		code += '-'
		i = random.randint(-10, 10)
		if i < 2:
			code += 'M'
		else:
			code += 'Z'
		code += str(user_id)[len(str(user_id))-1]
		i = random.randint(-10, 10)
		if i > 5:
			code += 'L'
		else:
			code += '0'
		code += '-'
		i = random.randint(-10, 10)
		if i < 2:
			code += 'S'
		else:
			code += '7'
		code += str(user_id)[len(str(user_id))-1]
		i = random.randint(-10, 9)
		if i > 5:
			code += i
		else:
			code += 'H'
		"""Добавляем нового подписчика"""
		with self.connection:
			self.cursor.execute("INSERT INTO `user_info` (`user_id`, `user_name`, `point` ) VALUES(?,?,?)", (user_id,user_name,1000))
			self.cursor.execute("INSERT INTO `promocode` (`code`, `user_id`) VALUES(?,?)", (code,user_id))
			self.cursor.execute("INSERT INTO `chek` (`user_id`) VALUES(?)", (user_id,))
			self.cursor.execute("INSERT INTO `proces` (`user_id`) VALUES(?)", (user_id,))

	def subscriber_exists(self, user_id):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			return bool(len(result))

	def balance(self, user_id):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			return result[0][3:5]

	def balance1(self, user_id):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			return result[0][3]

	def code(self,user_id, code):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `promocode` WHERE `code` = ?', (code,)).fetchall()
			if bool(len(result)) == True:
				if result[0][1] == user_id:
					return False
				else:
					if result[0][3] < 0:
						return True
					elif result [0][3] == 0:
						return False
					else:
						self.cursor.execute('UPDATE `promocode` SET `sroc` = ? WHERE `code` = ?', (result[0][3]-1, code))
						return True
			else:
				return False

	def code1(self, code):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `promocode` WHERE `code` = ?', (code,)).fetchall()
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (result[0][1],)).fetchall()
			return result[0][1:3]

	def chek(self, user_id):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			return result[0][5]

	def plus_point(self, user_id, sum):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]+sum, user_id))
			self.cursor.execute('UPDATE `user_info` SET `chek` = ? WHERE `user_id` = ?', (1, user_id))

	def plus_point_user(self, user_id, sum):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]+sum, user_id))
			self.cursor.execute('UPDATE `user_info` SET `bonus` = ? WHERE `user_id` = ?', (1, user_id))

	def output(self, user_id, type, money):
		with self.connection:
			self.cursor.execute('UPDATE `chek` SET `cheker1` = ? WHERE `user_id` = ?', (1, user_id))

	def get_cheker1(self, user_id):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `chek` WHERE `user_id` = ?', (user_id,)).fetchall()
			return result[0][2]

	def get_point(self, user_id):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			return result[0][4]

	def cazino(self, user_id, sum):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]-sum, user_id))
			if sum < 0:
				if result[0][8] == 2:
					result1 = self.cursor.execute('SELECT * FROM `proces` WHERE `user_id` = ?', (user_id,)).fetchall()
					self.cursor.execute('UPDATE `proces` SET `progress` = ? WHERE `user_id` = ?', (result1[0][2]-sum, user_id))
					if result1[0][2]-sum >= 500:
						self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]+400, user_id))
						self.cursor.execute('UPDATE `proces` SET `progress` = ? WHERE `user_id` = ?', (0, user_id))
						self.cursor.execute('UPDATE `proces` SET `cel` = ? WHERE `user_id` = ?', (1, user_id))
						self.cursor.execute('UPDATE `user_info` SET `quen` = ? WHERE `user_id` = ?', (3, user_id))
						return 2

				elif result[0][8] == 6:
					result1 = self.cursor.execute('SELECT * FROM `proces` WHERE `user_id` = ?', (user_id,)).fetchall()
					self.cursor.execute('UPDATE `proces` SET `progress` = ? WHERE `user_id` = ?', (result1[0][2]-sum, user_id))
					if result1[0][2]-sum >= 3000:
						self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]+1200, user_id))
						self.cursor.execute('UPDATE `proces` SET `progress` = ? WHERE `user_id` = ?', (0, user_id))
						self.cursor.execute('UPDATE `proces` SET `cel` = ? WHERE `user_id` = ?', (1000, user_id))
						self.cursor.execute('UPDATE `user_info` SET `quen` = ? WHERE `user_id` = ?', (7, user_id))
						return 4

				elif result[0][8] == 9:
					result1 = self.cursor.execute('SELECT * FROM `proces` WHERE `user_id` = ?', (user_id,)).fetchall()
					self.cursor.execute('UPDATE `proces` SET `progress` = ? WHERE `user_id` = ?', (result1[0][2]-sum, user_id))
					if result1[0][2]-sum >= 3000:
						self.cursor.execute('UPDATE `user_info` SET `balance` = ? WHERE `user_id` = ?', (result[0][3]+1, user_id))
						self.cursor.execute('UPDATE `proces` SET `progress` = ? WHERE `user_id` = ?', (0, user_id))
						self.cursor.execute('UPDATE `proces` SET `cel` = ? WHERE `user_id` = ?', (1, user_id))
						self.cursor.execute('UPDATE `user_info` SET `quen` = ? WHERE `user_id` = ?', (10, user_id))
						return 6

			if result[0][8] == 5:
				result1 = self.cursor.execute('SELECT * FROM `proces` WHERE `user_id` = ?', (user_id,)).fetchall()
				self.cursor.execute('UPDATE `proces` SET `progress` = ? WHERE `user_id` = ?', (result1[0][2]+1, user_id))
				if result1[0][2]+1 >= 10:
					self.cursor.execute('UPDATE `user_info` SET `balance` = ? WHERE `user_id` = ?', (result[0][3]+1, user_id))
					self.cursor.execute('UPDATE `proces` SET `progress` = ? WHERE `user_id` = ?', (0, user_id))
					self.cursor.execute('UPDATE `proces` SET `cel` = ? WHERE `user_id` = ?', (3000, user_id))
					self.cursor.execute('UPDATE `user_info` SET `quen` = ? WHERE `user_id` = ?', (6, user_id))
					return 3

			elif result[0][8] == 8:
				result1 = self.cursor.execute('SELECT * FROM `proces` WHERE `user_id` = ?', (user_id,)).fetchall()
				self.cursor.execute('UPDATE `proces` SET `progress` = ? WHERE `user_id` = ?', (result1[0][2]+1, user_id))
				if result1[0][2]+1 >= 20:
					self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]+2000, user_id))
					self.cursor.execute('UPDATE `proces` SET `progress` = ? WHERE `user_id` = ?', (0, user_id))
					self.cursor.execute('UPDATE `proces` SET `cel` = ? WHERE `user_id` = ?', (3000, user_id))
					self.cursor.execute('UPDATE `user_info` SET `quen` = ? WHERE `user_id` = ?', (9, user_id))
					return 5

	def stata(self):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `stata` WHERE `id` = ?', (1,)).fetchall()
			return result[0][1:3]

	def update_stata(self, id, count):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `stata` WHERE `id` = ?', (1,)).fetchall()
			self.cursor.execute('UPDATE `stata` SET `count` = ? WHERE `id` = ?', (count, 1))
			self.cursor.execute('UPDATE `stata` SET `id_p` = ? WHERE `id` = ?', (id, 1))

	def plus_balance(self, user_id, sum):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			if sum >= 490:
				if sum >= 990:
					self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]+300000, user_id))
				else:
					self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]+100000, user_id))

			sum = sum/2
			sum = sum - sum/100*5
			self.cursor.execute('UPDATE `user_info` SET `balance` = ? WHERE `user_id` = ?', (result[0][3]+int(sum), user_id))
			if result[0][8] == 10:
				self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]+70000, user_id))
				self.cursor.execute('UPDATE `user_info` SET `quen` = ? WHERE `user_id` = ?', (11, user_id))
				return 1

	def get_bonus(self):
		with self.connection:
			return self.cursor.execute("SELECT * FROM `user_info` WHERE `bonus` = ?", (1,)).fetchall()

	def update_bonus(self, user_id):
		with self.connection:
			self.cursor.execute('UPDATE `user_info` SET `bonus` = ? WHERE `user_id` = ?', (0, user_id))

	def get_user_bonus(self, user_id):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			return result[0][7]

	def doxod(self, user_id):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]+result[0][9], user_id))
			if result[0][8] == 1:
				result1 = self.cursor.execute('SELECT * FROM `proces` WHERE `user_id` = ?', (user_id,)).fetchall()
				self.cursor.execute('UPDATE `proces` SET `progress` = ? WHERE `user_id` = ?', (result1[0][2]+result[0][9], user_id))
				if result1[0][2]+result[0][9] >= 300:
					self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]+200, user_id))
					self.cursor.execute('UPDATE `proces` SET `progress` = ? WHERE `user_id` = ?', (0, user_id))
					self.cursor.execute('UPDATE `proces` SET `cel` = ? WHERE `user_id` = ?', (500, user_id))
					self.cursor.execute('UPDATE `user_info` SET `quen` = ? WHERE `user_id` = ?', (2, user_id))
					return 1, result[0][9]

			elif result[0][8] == 4:
				result1 = self.cursor.execute('SELECT * FROM `proces` WHERE `user_id` = ?', (user_id,)).fetchall()
				self.cursor.execute('UPDATE `proces` SET `progress` = ? WHERE `user_id` = ?', (result1[0][2]+1, user_id))
				if result1[0][2]+1 >= 30:
					self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]+1000, user_id))
					self.cursor.execute('UPDATE `proces` SET `progress` = ? WHERE `user_id` = ?', (0, user_id))
					self.cursor.execute('UPDATE `proces` SET `cel` = ? WHERE `user_id` = ?', (10, user_id))
					self.cursor.execute('UPDATE `user_info` SET `quen` = ? WHERE `user_id` = ?', (5, user_id))
					return 2, result[0][9]

			elif result[0][8] == 6:
				result1 = self.cursor.execute('SELECT * FROM `proces` WHERE `user_id` = ?', (user_id,)).fetchall()
				self.cursor.execute('UPDATE `proces` SET `progress` = ? WHERE `user_id` = ?', (result1[0][2]+result[0][9], user_id))
				if result1[0][2]+result[0][9] >= 3000:
					self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]+1200, user_id))
					self.cursor.execute('UPDATE `proces` SET `progress` = ? WHERE `user_id` = ?', (0, user_id))
					self.cursor.execute('UPDATE `proces` SET `cel` = ? WHERE `user_id` = ?', (1000, user_id))
					self.cursor.execute('UPDATE `user_info` SET `quen` = ? WHERE `user_id` = ?', (7, user_id))
					return 4, result[0][9]

			elif result[0][8] == 7:
				result1 = self.cursor.execute('SELECT * FROM `proces` WHERE `user_id` = ?', (user_id,)).fetchall()
				self.cursor.execute('UPDATE `proces` SET `progress` = ? WHERE `user_id` = ?', (result1[0][2]+result[0][9], user_id))
				if result1[0][2]+result[0][9] >= 1000:
					self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]+1500, user_id))
					self.cursor.execute('UPDATE `proces` SET `progress` = ? WHERE `user_id` = ?', (0, user_id))
					self.cursor.execute('UPDATE `proces` SET `cel` = ? WHERE `user_id` = ?', (20, user_id))
					self.cursor.execute('UPDATE `user_info` SET `quen` = ? WHERE `user_id` = ?', (8, user_id))
					return 5, result[0][9]

			return 0,result[0][9]

	def bizno3s(self, user_id):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			if result[0][6] == 1:
				if result[0][4] >= 10000:
					self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]-10000, user_id))
					self.cursor.execute('UPDATE `user_info` SET `biznos` = ? WHERE `user_id` = ?', (2, user_id))
					self.cursor.execute('UPDATE `user_info` SET `doxod` = ? WHERE `user_id` = ?', (20, user_id))
					self.cursor.execute('UPDATE `user_info` SET `doxod_has` = ? WHERE `user_id` = ?', (60, user_id))
					return True
				else:
					return False
			elif result[0][6] == 2:
				if result[0][4] >= 15000:
					self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]-15000, user_id))
					self.cursor.execute('UPDATE `user_info` SET `biznos` = ? WHERE `user_id` = ?', (3, user_id))
					self.cursor.execute('UPDATE `user_info` SET `doxod` = ? WHERE `user_id` = ?', (35, user_id))
					self.cursor.execute('UPDATE `user_info` SET `doxod_has` = ? WHERE `user_id` = ?', (100, user_id))
					return True
				else:
					return False
			elif result[0][6] == 3:
				if result[0][4] >= 30000:
					self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]-30000, user_id))
					self.cursor.execute('UPDATE `user_info` SET `biznos` = ? WHERE `user_id` = ?', (4, user_id))
					self.cursor.execute('UPDATE `user_info` SET `doxod` = ? WHERE `user_id` = ?', (50, user_id))
					self.cursor.execute('UPDATE `user_info` SET `doxod_has` = ? WHERE `user_id` = ?', (120, user_id))
					return True
				else:
					return False
			elif result[0][6] == 4:
				if result[0][4] >= 45000:
					self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]-45000, user_id))
					self.cursor.execute('UPDATE `user_info` SET `biznos` = ? WHERE `user_id` = ?', (5, user_id))
					self.cursor.execute('UPDATE `user_info` SET `doxod` = ? WHERE `user_id` = ?', (75, user_id))
					self.cursor.execute('UPDATE `user_info` SET `doxod_has` = ? WHERE `user_id` = ?', (150, user_id))
					return True
				else:
					return False
			elif result[0][6] == 5:
				if result[0][4] >= 80000:
					self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]-80000, user_id))
					self.cursor.execute('UPDATE `user_info` SET `biznos` = ? WHERE `user_id` = ?', (6, user_id))
					self.cursor.execute('UPDATE `user_info` SET `doxod` = ? WHERE `user_id` = ?', (130, user_id))
					self.cursor.execute('UPDATE `user_info` SET `doxod_has` = ? WHERE `user_id` = ?', (200, user_id))
					return True
				else:
					return False
			elif result[0][6] == 6:
				if result[0][4] >= 140000:
					self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]-140000, user_id))
					self.cursor.execute('UPDATE `user_info` SET `biznos` = ? WHERE `user_id` = ?', (7, user_id))
					self.cursor.execute('UPDATE `user_info` SET `doxod` = ? WHERE `user_id` = ?', (210, user_id))
					self.cursor.execute('UPDATE `user_info` SET `doxod_has` = ? WHERE `user_id` = ?', (250, user_id))
					return True
				else:
					return False
			elif result[0][6] == 7:
				if result[0][4] >= 300000:
					self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]-300000, user_id))
					self.cursor.execute('UPDATE `user_info` SET `biznos` = ? WHERE `user_id` = ?', (8, user_id))
					self.cursor.execute('UPDATE `user_info` SET `doxod` = ? WHERE `user_id` = ?', (240, user_id))
					self.cursor.execute('UPDATE `user_info` SET `doxod_has` = ? WHERE `user_id` = ?', (270, user_id))
					return True
				else:
					return False
			elif result[0][6] == 8:
				if result[0][4] >= 1000000:
					self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]-1000000, user_id))
					self.cursor.execute('UPDATE `user_info` SET `biznos` = ? WHERE `user_id` = ?', (9, user_id))
					self.cursor.execute('UPDATE `user_info` SET `doxod` = ? WHERE `user_id` = ?', (400, user_id))
					self.cursor.execute('UPDATE `user_info` SET `doxod_has` = ? WHERE `user_id` = ?', (700, user_id))
					return True
				else:
					return False
			else:
				return 5

	def qw3(self, user_id):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			if result[0][8] == 3:
				result1 = self.cursor.execute('SELECT * FROM `proces` WHERE `user_id` = ?', (user_id,)).fetchall()
				self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]+800, user_id))
				self.cursor.execute('UPDATE `proces` SET `progress` = ? WHERE `user_id` = ?', (0, user_id))
				self.cursor.execute('UPDATE `proces` SET `cel` = ? WHERE `user_id` = ?', (30, user_id))
				self.cursor.execute('UPDATE `user_info` SET `quen` = ? WHERE `user_id` = ?', (4, user_id))
				return 1

	def coder(self, user_id):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `promocode` WHERE `user_id` = ?', (user_id,)).fetchall()
			return result[0][2]

	def qio(self, user_id):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			result1 = self.cursor.execute('SELECT * FROM `proces` WHERE `user_id` = ?', (user_id,)).fetchall()
			if result[0][8] == 11:
				return False
			if result[0][8] == 1:
				a = "Заработать 300 🧿 "
				b = "200 🧿"
				c = 300
			elif result[0][8] == 2:
				a = "Выиграть 500 🧿 в колесе фортуны"
				b = "400 🧿"
				c = 500
			elif result[0][8] == 3:
				a = "Купить новый бизнес"
				b = "800 🧿 "
				c = 1
			elif result[0][8] == 4:
				a = "Работать 30 раз"
				b = "1000 🧿 "
				c = 30
			elif result[0][8] == 5:
				a = "Прокрутить колесо фортуны 10 раз"
				b = "1 голда "
				c = 10
			elif result[0][8] == 6:
				a = "Накопить 3000 🧿 "
				b = "1200 🧿 "
				c = 3000
			elif result[0][8] == 7:
				a = "Заработать 1000 🧿 "
				b = "1500 🧿 "
				c = 1000
			elif result[0][8] == 8:
				a = "Прокрутить колесо фортуны 20 раз"
				b = "2000 🧿 "
				c = 20
			elif result[0][8] == 9:
				a = "Выиграть 3000 🧿 в колесе фортуны"
				b = "1 голда "
				c = 3000
			elif result[0][8] == 10:
				a = 'Купить 75 голды (Раздел "Пополнить")'
				b = "70000 🧿"
				c = 75

			return result[0][8],a,b,result1[0][2],c

	def get_ckek(self):
		with self.connection:
			return self.cursor.execute("SELECT * FROM `user_info` WHERE `chek1` = ?", (1,)).fetchall()

	def update_doxod(self, user_id):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4]+result[0][10], user_id))
			return result[0][10]

	def minys_bakance(self, user_id, min):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			self.cursor.execute('UPDATE `user_info` SET `balance` = ? WHERE `user_id` = ?', (result[0][3] - min, user_id))

	def minys_bakance_point(self, user_id, min):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4] - min, user_id))

	def plus_bakance(self, user_id, min):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			self.cursor.execute('UPDATE `user_info` SET `balance` = ? WHERE `user_id` = ?', (result[0][3] + min, user_id))

	def plus_bakance_point(self, user_id, min):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			self.cursor.execute('UPDATE `user_info` SET `point` = ? WHERE `user_id` = ?', (result[0][4] + min, user_id))

	def add_code(self, code, col = -1):
		with self.connection:
			self.cursor.execute("INSERT INTO `promocode` (`code`, `user_id`, `sroc`) VALUES(?,?,?)", (code, 1, col))

	def biznos(self, user_id):
		with self.connection:
			result = self.cursor.execute('SELECT * FROM `user_info` WHERE `user_id` = ?', (user_id,)).fetchall()
			if result[0][6] == 1:
				return '(Ваш бизнес)','','','','','','','','',result[0][10],result[0][9]
			if result[0][6] == 2:
				return '','(Ваш бизнес)','','','','','','','',result[0][10],result[0][9]
			if result[0][6] == 3:
				return '','','(Ваш бизнес)','','','','','','',result[0][10],result[0][9]
			if result[0][6] == 4:
				return '','','','(Ваш бизнес)','','','','','',result[0][10],result[0][9]
			if result[0][6] == 5:
				return '','','','','(Ваш бизнес)','','','','',result[0][10],result[0][9]
			if result[0][6] == 6:
				return '','','','','','(Ваш бизнес)','','','',result[0][10],result[0][9]
			if result[0][6] == 7:
				return '','','','','','','(Ваш бизнес)','','',result[0][10],result[0][9]
			if result[0][6] == 8:
				return '','','','','','','','(Ваш бизнес)','',result[0][10],result[0][9]
			if result[0][6] == 9:
				return '','','','','','','','','(Ваш бизнес)',result[0][10],result[0][9]



