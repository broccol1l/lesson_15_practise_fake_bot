import telebot
import buttons as bt
import database as db

bot = telebot.TeleBot(token="7365056271:AAGYXlXsFlg-rkbccuo7cOIZ-N4dpIajhdU")
users = {}

#db.add_product(pr_name="Chicken Donar", pr_desc="The best", pr_price=30000, pr_quantity=9, pr_photo="https://чайхана-дзр.рф/wp-content/uploads/2018/09/doner-chiken.jpg")
#db.add_product(pr_name="Lavash", pr_desc="The bestie", pr_price=30000, pr_quantity=9, pr_photo="https://avatars.mds.yandex.net/get-sprav-products/9685839/2a00000188b586064be748d4713c1b0912eb/M_height")
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    checker = db.check_user(user_id)
    if checker == True:
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.main_menu_kb())
    elif checker == False:
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
                                  f"Место проживания: {location}"
                                  f"Выберите действие", reply_markup=bt.main_menu_kb())
        db.add_user(user_id, name, number)
    else:
        bot.send_message(user_id, "Отправьте свою локацию через кнопку",
                         reply_markup=bt.location_bt())
        bot.register_next_step_handler(message, get_location, name, number)

@bot.callback_query_handler(lambda call: "prod_" in call.data)
def product_call(call):
    user_id = call.message.chat.id
    bot.delete_message(user_id, call.message.message_id)
    product_id = int(call.data.replace("prod_", ""))
    product_info = db.get_exact_product(product_id)
    users[user_id] = {"pr_id": product_id, "pr_name": product_info[0], "pr_count":1, "pr_price": product_info[1]}
    bot.send_photo(user_id, photo=product_info[3], caption=f"{product_info[0]}\n\n"
                                                           f"Описание: {product_info[2]}\n"
                                                           f"Цена : {product_info[1]} сум",
                   reply_markup=bt.exact_product())

@bot.callback_query_handler(lambda call: call.data in ["main_menu", "cart", "minus", "plus", "none", "back",
                                                       "to_cart"])
def all_calls(call):
    user_id = call.message.chat.id
    if call.data == "main_menu":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.main_menu_kb())
    elif call.data == "cart":
        cart = db.get_cart_id_name(user_id)
        user_cart = db.get_user_cart(user_id)
        full_text = f"Ваша корзина: \n\n"
        total_amount = 0
        for i in user_cart:
            full_text += f"{i[0]} x{i[1]} = {i[2]}\n"
            total_amount += i[2]
        full_text += f"\n\nИтоговая сумма: {total_amount}"
        bot.send_message(user_id, text=full_text, reply_markup=bt.get_cart_kb(cart))
    elif call.data == "plus":
        current_amount = users[user_id]["pr_count"]
        users[user_id]["pr_count"] += 1
        bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id,
                                      reply_markup=bt.exact_product(current_amount=current_amount,
                                                                    plus_or_minus="plus"))
    elif call.data == "minus":
        current_amount = users[user_id]["pr_count"]
        if current_amount > 1:
            users[user_id]["pr_count"] -= 1
            bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id,
                                          reply_markup=bt.exact_product(current_amount=current_amount,
                                                                        plus_or_minus="minus"))
        else:
            pass
    elif call.data == "none":
        pass
    elif call.data == "back":
        bot.delete_message(user_id, call.message.message_id)
        # users.pop(user_id)
        all_product = db.get_pr_id_name()
        bot.send_message(user_id, "Выберите продукт", reply_markup=bt.products_in(all_product))
    elif call.data == "to_cart":
        db.add_to_cart(user_id, users[user_id]["pr_id"], users[user_id]["pr_name"],
                       users[user_id]["pr_count"], users[user_id]["pr_price"])
        users.pop(user_id)
        bot.delete_message(user_id, call.message.message_id)
        all_product = db.get_pr_id_name()
        bot.send_message(user_id, "Продукт добавлен в корзину. Выберите продукт",
                         reply_markup=bt.products_in(all_product))


# DZ RUS-UZB
@bot.callback_query_handler(lambda call: True)
def language_call(call):
    user_id = call.from_user.id
    bot.delete_message(user_id, call.message.message_id)
    if call.data == "lang_rus":
        bot.send_message(user_id, "Вы переключились на русский язык")
    elif call.data == "lang_uzb":
        bot.send_message(user_id, "Siz o'zbek tilini tanladingiz")


@bot.message_handler(content_types=["text"])
def main_menu(message):
    user_id = message.from_user.id
    text = message.text
    if text == "🍽Меню":
        all_product = db.get_pr_id_name()
        bot.send_message(user_id, "Выберите продукт", reply_markup=bt.products_in(all_product))
    elif text == "🛒Корзина":
        bot.send_message(user_id, "Ваша корзина")
    elif text == "✍️Оставить отзыв":
        bot.send_message(user_id, "Напишите свой отзыв")
    elif text == "Изменить язык":
        bot.send_message(user_id, "Какой язык хотите поставить?", reply_markup=bt.language_in())





bot.infinity_polling()
