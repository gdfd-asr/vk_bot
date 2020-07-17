from vkbottle import Bot, Message
import asyncio, requests, json
import config
import random
import time as tm
from sqlighter import SQLighter
import logging
import keyboards as kb
from vkbottle.api import API
from vkbottle.api.api.util.builtin import LimitedTokenGenerator
from datetime import datetime, date,time,timedelta
from vkbottle.exceptions import VKError
import os
from vkbottle.rule import AbstractMessageRule

token = "053bc3be3550cb649bb2"

bot = Bot(config.API_TOKEN, debug=False)

# инициализируем соединение с БД
db = SQLighter('db.db')

#id админа
admin_id = 111182681

#cсылка на донаты
link = 'https://vk.com/app6471849_-187582264'
link2 = f'https://api.vkdonate.ru?action=donates&count=50&sort=date&key={token}'
link3 = f'https://vkdonate.ru/api?action=donates&count=50&sort=date&key={token}'

# Создаем класс для правила
class OnlyMe(AbstractMessageRule):
	async def check(self, message: Message):
		# Функция check вызывается при проверке правила
		if message.from_id == admin_id: # Если пользователь, написавший сообщение имеет id = admin_id
			return True # Проверка пройдена

@bot.on.message(OnlyMe(), text="/admin")
async def wrapper(ans: Message):
	await ans("Команды доступна для админа", keyboard = kb.kb4())

@bot.on.message(OnlyMe(), text="Снять 💰 у пользователя")
async def wrapper(ans: Message):
	await ans("Введите id пользователя и сколько нужно снять\nПример: 1392393 40", keyboard = kb.back())
	await bot.branch.add(ans.peer_id, "minus")

@bot.on.message(OnlyMe(), text="Снять 🧿 у пользователя")
async def wrapper(ans: Message):
	await ans("Введите id пользователя и сколько нужно снять\nПример: 1392393 40", keyboard = kb.back())
	await bot.branch.add(ans.peer_id, "minus_point")

@bot.on.message(OnlyMe(), text="Пополнить 💰 у пользователя")
async def wrapper(ans: Message):
	await ans("Введите id пользователя и на сколько нужно пополнить\nПример: 1392393 40", keyboard = kb.back())
	await bot.branch.add(ans.peer_id, "plus")

@bot.on.message(OnlyMe(), text="Пополнить 🧿 у пользователя")
async def wrapper(ans: Message):
	await ans("Введите id пользователя и на сколько нужно пополнить\nПример: 1392393 40", keyboard = kb.back())
	await bot.branch.add(ans.peer_id, "plus_point")

@bot.on.message(OnlyMe(), text="Массовая рассылка")
async def wrapper(ans: Message):
	await ans("Введите сообщение которое хотите разослать всем", keyboard = kb.back())
	await bot.branch.add(ans.peer_id, "mas")

@bot.on.message(OnlyMe(), text="Создать промокод")
async def wrapper(ans: Message):
	await ans("Введите промокд и количесвто использований\n Пример SDA-QRT-E3T 50", keyboard = kb.back())
	await bot.branch.add(ans.peer_id, "code")

@bot.branch.simple_branch("code")
async def branch(ans: Message):
	if ans.text.lower() == "назад":
		await ans("Возвращаю в главное меню", keyboard = kb.kb4())
		await bot.branch.exit(ans.peer_id)
	else:
		try:
			d = ans.text.split()
			db.add_code(d[0],int(d[1]))
			await ans(f"Промокод {d[0]} на {d[1]} использований, добавлен!", keyboard = kb.kb4())
			await bot.branch.exit(ans.peer_id)
	
		except Exception as e:
			await ans("Не вверно введены данные, попробуйте ещё раз или нажмите назад")

@bot.branch.simple_branch("mas")
async def branch(ans: Message):
	if ans.text.lower() == "назад":
		await ans("Возвращаю в главное меню", keyboard = kb.kb4())
		await bot.branch.exit(ans.peer_id)
	else:
		await ans("Рассылка начилась", keyboard = kb.kb4())
		await bot.branch.exit(ans.peer_id)
		for i in db.get_ckek():
			try:
				await bot.api.messages.send(
					peer_id=i[1],
					message=ans.text,
					random_id=bot.extension.random_id())
			except Exception as e:
				print('erro')
		await ans("Рассылка закончилась")

@bot.branch.simple_branch("minus")
async def branch(ans: Message):
	if ans.text.lower() == "назад":
		await ans("Возвращаю в главное меню", keyboard = kb.kb4())
		await bot.branch.exit(ans.peer_id)
	else:
		try:
			d = ans.text.split()
			db.minys_bakance(int(d[0]), int(d[1]))
			await ans(f"У пользователя {d[0]}\nСнято с баланса(💰) {d[1]}", keyboard = kb.kb4())
			await bot.branch.exit(ans.peer_id)
		except Exception as e:
			await ans("Не верно введены данные, попробуйте ещё раз или нажмите назад")

@bot.branch.simple_branch("minus_point")
async def branch(ans: Message):
	if ans.text.lower() == "назад":
		await ans("Возвращаю в главное меню", keyboard = kb.kb4())
		await bot.branch.exit(ans.peer_id)
	else:
		try:
			d = ans.text.split()
			db.minys_bakance_point(int(d[0]), int(d[1]))
			await ans(f"У пользователя {d[0]}\nСнято с баланса(🧿) {d[1]}", keyboard = kb.kb4())
			await bot.branch.exit(ans.peer_id)
		except Exception as e:
			await ans("Не верно введены данные, попробуйте ещё раз или нажмите назад")


@bot.branch.simple_branch("plus")
async def branch(ans: Message):
	if ans.text.lower() == "назад":
		await ans("Возвращаю в главное меню", keyboard = kb.kb4())
		await bot.branch.exit(ans.peer_id)
	else:
		try:
			d = ans.text.split()
			db.plus_bakance(int(d[0]), int(d[1]))
			await ans(f"У пользователя {d[0]}\nСнято с баланса(💰) {d[1]}", keyboard = kb.kb4())
			await bot.branch.exit(ans.peer_id)
		except Exception as e:
			await ans("Не верно введены данные, попробуйте ещё раз или нажмите назад")

@bot.branch.simple_branch("plus_point")
async def branch(ans: Message):
	if ans.text.lower() == "назад":
		await ans("Возвращаю в главное меню", keyboard = kb.kb4())
		await bot.branch.exit(ans.peer_id)
	else:
		try:
			d = ans.text.split()
			db.plus_bakance_point(int(d[0]), int(d[1]))
			await ans(f"У пользователя {d[0]}\nСнято с баланса(🧿) {d[1]}", keyboard = kb.kb4())
			await bot.branch.exit(ans.peer_id)
		except Exception as e:
			await ans("Не верно введены данные, попробуйте ещё раз или нажмите назад")

@bot.branch.simple_branch("qiwi")
async def branch(ans: Message):
	if ans.text.lower() == "назад":
		await ans("Возвращаю в главное меню", keyboard = kb.kb0())
		await bot.branch.exit(ans.peer_id)
	else:
		await ans("Ваша заявка принята😊", keyboard = kb.kb0())
		db.output(ans.peer_id)
		await bot.branch.exit(ans.peer_id)

@bot.branch.simple_branch("carta")
async def branch(ans: Message):
	if ans.text.lower() == "назад":
		await ans("Возвращаю в главное меню", keyboard = kb.kb0())
		await bot.branch.exit(ans.peer_id)
	else:
		await ans("Ваша заявка принята😊", keyboard = kb.kb0())
		db.output(ans.peer_id)
		await bot.branch.exit(ans.peer_id)

@bot.branch.simple_branch("yandex")
async def branch(ans: Message):
	if ans.text.lower() == "назад":
		await ans("Возвращаю в главное меню", keyboard = kb.kb0())
		await bot.branch.exit(ans.peer_id)

	else:
		await ans("Ваша заявка принята😊", keyboard = kb.kb0())
		db.output(ans.peer_id)
		await bot.branch.exit(ans.peer_id)

@bot.on.message()
async def wrapper(ans: Message):
	response = ans.text
	user_id = ans.peer_id
	if(not db.subscriber_exists(user_id)):
		user_info = await bot.api.users.get(user_id, name_case="gen")
		user_name = user_info[0].first_name
		user_surname = user_info[0].last_name
		user_name = user_name +' '+user_surname
		db.add_db(user_id,user_name)
		await ans('За регистрацию в боте мы дарим вам 1000🧿', keyboard = kb.kb0())
	if response.lower() == 'начать':
		await ans('Это главная страница. Ты можешь выбрать любое действие на клавиатуре!', keyboard = kb.kb0())

	elif response.lower() == 'баланс 💳':
		a,b = db.balance(user_id)
		await ans('Баланс 💳: \nНа вашем балансе:\n{:.0f}🧿 ( ={:.0f} руб. ) \n {:.0f} 💰'.format(b,b/100,a), keyboard = kb.kb1(link))

	elif response.lower() == 'работать 🤖':
		f,c = db.doxod(user_id)
		if f == 1:
			await ans('Задание пройдено!\nВы получаете награду: 200🧿')
		elif f == 2:
			await ans('Задание пройдено!\nВы получаете награду: 1000🧿')
		elif f == 4:
			await ans('Задание пройдено!\nВы получаете награду: 1200🧿')
		elif f == 5:
			await ans('Задание пройдено!\nВы получаете награду: 1200🧿')

		await ans(f'Вы заработали {c} (🧿)')

	elif response.lower() == 'вывести деньги (🧿)':
		if db.balance1(user_id) >= 75:
			if db.get_cheker1(user_id) == 0:
				await ans('Выберите реквизиты ', keyboard = kb.kb2())
			else:
				await ans('Вы уже отправили заявку на вывод средств')
		else:
			await ans('Недостаточно голды (💰) для вывода средств.У вас на балансе должно быть как минимум 75 баксов!💸 Купить голду можно в разделе Баланс')

	elif response.lower() == 'киви':
		await ans('Введите свои реквезиты и ожидайте когда модерация расмотрит вашу заявку', keyboard = kb.back())
		await bot.branch.add(ans.peer_id, "qiwi")

	elif response.lower() == 'карта':
		await ans('Введите свои реквезиты и ожидайте когда модерация расмотрит вашу заявку', keyboard = kb.back())
		await bot.branch.add(ans.peer_id, "carta")

	elif response.lower() == 'яндекс деньги':
		await ans('Введите свои реквезиты и ожидайте когда модерация расмотрит вашу заявку', keyboard = kb.back())
		await bot.branch.add(ans.peer_id, "yandex")

	elif response.lower() == 'назад':
		await ans('Это главная страница. Ты можешь выбрать любое действие на клавиатуре!', keyboard = kb.kb0())

	elif response.lower() == '❓ зачем нужен донат':
		await ans('vk.com/@-187582264-dlya-chego')

	elif response.lower() == 'промокод 🏷':
		await ans(f'Твой промокод {db.coder(user_id)}')

	elif response.lower() == 'казино 🎱':
		if db.get_point(user_id) >= 300:
			sum = random.randint(100, 900)
			f = db.cazino(user_id, 300-sum)
			if f == 2:
				await ans('Задание пройдено!\nВы получаете награду: 400🧿')
			elif f == 3:
				await ans('Задание пройдено!\nВы получаете награду: 1💰')
			elif f == 4:
				await ans('Задание пройдено!\nВы получаете награду: 1200🧿')
			elif f == 5:
				await ans('Задание пройдено!\nВы получаете награду: 2000🧿')
			elif f == 6:
				await ans('Задание пройдено!\nВы получаете награду: 1💰')

			await ans("Добро пожадывать в казино 'Фортуна'\n Вы поставили 300🧿\nИ вы выиграли {}🧿".format(sum))
		else:
			await ans("Вам не хватает 🧿, нужно 300🧿 для ставки")

	elif response.lower() == 'бизнесы 📦':
		a,b,d,f,j,g,h,q,w,m,n = db.biznos(user_id)
		await ans("Бизнесы 📦: \n1 - Точка кофе ☕ {} \n2 - Продуктовый магазин 🍏 {}\n3 - Компьютерный клуб 💻 {} \n4 - Пятёрочка ⃣ {}\n5 - Магазин Adidas 👟 {}\n6 - KFS 🐔 {} \n7 - Макдональдс 🍟 {} \n8 - Автосалон Tesla 🚗 {}\n9 - Компания SpaceX 🚀 {}\n\nВаш доход в час {}🧿\nВаш доход за работу {}🧿".format(a,b,d,f,j,g,h,q,w,m,n) , keyboard = kb.kb3())

	elif response.lower() == 'купить бизнес 📈':
		d = db.bizno3s(user_id) 
		if d == True:
			await ans('Вы приобрели новый бизнес')
			if db.qw3(user_id) == 1:
				await ans('Задание пройдено!\nВы получаете награду: 800🧿')
		elif d == 5:
			await ans('У вас максимальный бизнес')
		else:
			await ans('У вас не хватает 🧿')

	elif response.lower() == 'ежедневный бонус 🎁':
		if db.get_user_bonus(user_id) == 0:
			sum = random.randint(500, 3000)
			await ans("Вам выпало {}🧿".format(sum))
			db.plus_point_user(user_id, sum)
		else:
			await ans("У вас уже получин ежедневный бонус!")

	elif response.lower() == 'задания 📌':
		if db.qio(user_id) == False   :
			await ans("Все задания выполнены!")
		else:
			a,b,c,h,g = db.qio(user_id)
			await ans("📌 Задание {}/10: \n{}\n\nНаграда: {}\nПрогресс: {}/{}".format(a,b,c,h,g))

	else:
		if db.chek(user_id) == 0:
			if(not db.code(user_id, response)):
				await ans('К сожалению, такого промокода не существует(')
			else:
				id,name = db.code1(response)
				if id == 1:
					await ans('Вы ввели промокод! Вы получаете 1000🧿'.format(id,name))
				else:
					await ans('Вы ввели промокод @id{}({})! Вы получаете 1000🧿'.format(id,name))
				db.plus_point(user_id,1000)
		else:
			await ans('Список команд ты можешь увидеть на клавиатуре!')

@bot.error_handler.error_handler(6)
async def rps_handler(e: VKError):
	await sleep(1)
	await e.method_requested(**e.params_requested)

async def scheduled(wait_for):
	count,id = db.stata()
	while True:
		await asyncio.sleep(wait_for)
		response = requests.get(link2)
		if response.status_code == 200:
			qde = response.json()
			if qde['count'] > count:
				for i in range(0,len(qde['donates'])):
					edq = qde['donates'][i]['id']
					user_id = qde['donates'][i]['uid']
					sum = qde['donates'][i]['sum']
					if id == edq:
						id = qde['donates'][0]['id']
						break
					else:
						if db.plus_balance(user_id, sum) == 1:
							await bot.api.messages.send(
								peer_id=user_id,
								message="Задание пройдено!\nВы получаете награду: 70000🧿",
								random_id=bot.extension.random_id())
						else:
							await bot.api.messages.send(
								peer_id=user_id,
								message="Ваш баланс 💰 пополнен!",
								random_id=bot.extension.random_id())
				count = qde['count']

		else:
			response = requests.get(link3)
			if response.status_code != 200:
				print('Ошибка донатов, сервер не отвечает')
			else:
				qde = response.json()
				if qde['count'] > count:
					for i in range(0,len(qde['donates'])):
						edq = qde['donates'][i]['id']
						user_id = qde['donates'][i]['uid']
						sum = qde['donates'][i]['sum']
						if id == qde:
							id = qde['donates'][0]['id']
							break
						else:
							if db.plus_balance(user_id, sum) == 1:
								await bot.api.messages.send(
									peer_id=user_id,
									message="Задание пройдено!\nВы получаете награду: 70000🧿",
									random_id=bot.extension.random_id())
							else:
								await bot.api.messages.send(
									peer_id=user_id,
									message="Ваш баланс 💰 пополнен!",
									random_id=bot.extension.random_id())
					count = qde['count']

		db.update_stata(id,count)

async def update():
	now = datetime.now()
	today = now.replace(hour=23, minute=54, second=59, microsecond=0)
	n = 0
	print(now)
	print(today)
	while True:
		now = datetime.now()
		await asyncio.sleep(5)
		n += 5
		if now > today:
			for i in db.get_bonus():
				db.update_bonus(i[1])
			await asyncio.sleep(600)
			now = datetime.now()
			today = now.replace(hour=23, minute=54, second=59, microsecond=0)
			print(now)
			print(today)
		if n >= 3600:
			n = 0
			for i in db.get_ckek():
				await bot.api.messages.send(
					peer_id=i[1],
					message=f"Ваш баланс пополнен на{db.update_doxod(i[1])}🧿",
					random_id=bot.extension.random_id())

if __name__ == '__main__':
	bot.loop.create_task(scheduled(10))
	bot.loop.create_task(update())
	bot.run_polling(skip_updates=False)
