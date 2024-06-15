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

def main_menu_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    products = types.KeyboardButton(text="🍽Меню")
    cart = types.KeyboardButton(text="🛒Корзина")
    feedback = types.KeyboardButton(text="✍️Оставить отзыв")
    language = types.KeyboardButton(text="Изменить язык")
    kb.add(products, cart, feedback, language)
    return kb

def language_in():
    kb = types.InlineKeyboardMarkup(row_width=2)

    rus = types.InlineKeyboardButton(text="🇷🇺Русский Язык", callback_data="lang_rus")
    uzb = types.InlineKeyboardButton(text="🇺🇿O'zbek Tili", callback_data="lang_uzb" )

    kb.add(rus, uzb)
    return kb
def products_in(all_products):
    kb = types.InlineKeyboardMarkup(row_width=2)
    main_menu = types.InlineKeyboardButton(text="Главное меню", callback_data="main_menu")
    cart = types.InlineKeyboardButton(text="Корзина", callback_data="cart")

    all_buttons = [types.InlineKeyboardButton(text=product[1], callback_data=f"prod_{product[0]}")
                   for product in all_products]
    kb.add(*all_buttons)
    kb.row(cart)
    kb.row(main_menu)
    return kb