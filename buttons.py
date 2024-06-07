from telebot import types
def phone_number_bt():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Поделись контактом",
                                  request_contact=True)
    kb.add(button)
    return kb

def location_bt():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Поделись локацией",
                                  request_location=True)
    kb.add(button)
    return kb