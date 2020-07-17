from vkbottle.api.keyboard import Keyboard, Text, OpenLink



def kb0():

	keyboard = Keyboard(inline=False)
	keyboard.add_row()
	keyboard.add_button(Text("Баланс 💳"), color="secondary")
	keyboard.add_button(Text("Бизнесы 📦"), color="secondary")
	keyboard.add_row()
	keyboard.add_button(Text("Казино 🎱"), color="secondary")
	keyboard.add_button(Text("Задания 📌"), color="secondary")
	keyboard.add_row()
	keyboard.add_button(Text("Работать 🤖"), color="secondary")
	keyboard.add_button(Text("Промокод 🏷"), color="secondary")
	keyboard.add_row()
	keyboard.add_button(Text("Ежедневный бонус 🎁"), color="primary")

	keyboard.generate()

	return keyboard

def kb1(link):

	keyboard = Keyboard(inline=False)
	keyboard.add_row()
	keyboard.add_button(OpenLink(label= "Купить голду (💰)", link= link))
	keyboard.add_button(Text("Вывести деньги (🧿)"), color="primary")
	keyboard.add_row()
	keyboard.add_button(Text("❓ Зачем нужен донат"), color="primary")
	keyboard.add_row()
	keyboard.add_button(Text("Назад"), color="negative")

	keyboard.generate()

	return keyboard

def kb2():

	keyboard = Keyboard(inline=False)
	keyboard.add_row()
	keyboard.add_button(Text("Яндекс деньги"), color="primary")
	keyboard.add_button(Text("Карта"), color="primary")
	keyboard.add_button(Text("Киви"), color="primary")
	keyboard.add_row()
	keyboard.add_button(Text("Назад"), color="negative")

	keyboard.generate()

	return keyboard

def kb3():
	keyboard = Keyboard(inline=False)
	keyboard.add_row()
	keyboard.add_button(Text("Купить бизнес 📈"), color="secondary")
	keyboard.add_row()
	keyboard.add_button(Text("Назад"), color="negative")

	keyboard.generate()

	return keyboard

def kb4():
	keyboard = Keyboard(inline=False)
	keyboard.add_row()
	keyboard.add_button(Text("Снять 💰 у пользователя"), color="secondary")
	keyboard.add_row()
	keyboard.add_button(Text("Снять 🧿 у пользователя"), color="secondary")
	keyboard.add_row()
	keyboard.add_button(Text("Пополнить 💰 у пользователя"), color="secondary")
	keyboard.add_row()
	keyboard.add_button(Text("Пополнить 🧿 у пользователя"), color="secondary")
	keyboard.add_row()
	keyboard.add_button(Text("Массовая рассылка"), color="secondary")
	keyboard.add_row()
	keyboard.add_button(Text("Создать промокод"), color="secondary")
	keyboard.add_row()
	keyboard.add_button(Text("Назад"), color="negative")

	keyboard.generate()

	return keyboard

def back():

	keyboard = Keyboard(inline= False)
	keyboard.add_row()
	keyboard.add_button(Text("Назад"), color = "negative")

	keyboard.generate()

	return keyboard