import telebot
import buttons as bt

bot = telebot.TeleBot(token="7365056271:AAGYXlXsFlg-rkbccuo7cOIZ-N4dpIajhdU")

@bot.message_handler(content_types=[""])

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Добро пожаловать в GARRY FOOD!\n"
                              "Напишите пожалуйста свое имя")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, "Отправьте пожалуйста свой номер телефона",
                     reply_markup=bt.phone_number_bt())
    bot.register_next_step_handler(message, get_number, name)

def get_number(message, name):
    user_id = message.from_user.id
    if message.contact:
        number = message.contact.phone_number
        print(name, number)
        bot.send_message(user_id, "Отправьте свою локацию",
                         reply_markup=bt.location_bt())
        bot.register_next_step_handler(message, get_location, name, number)
    else:
        bot.send_message(user_id, "Отправьте пожалуйста свой номер телефона через кнопку",
                         reply_markup=bt.phone_number_bt())
        bot.register_next_step_handler(message, get_number, name)
def get_location(message, name, number):
    user_id = message.from_user.id
    if message.location:
        location = message.location
        bot.send_message(user_id, f"Регистрация в GARRY FOOD успешно пройдена😋"
                                  f"Ваши данные:\n"
                                  f"Имя: {name}\n"
                                  f"Номер телефона: {number}\n"
                                  f"Место проживания: {location}")
    else:
        bot.send_message(user_id, "Отправьте свою локацию через кнопку",
                         reply_markup=bt.location_bt())
        bot.register_next_step_handler(message, get_location, name, number)



bot.infinity_polling()
