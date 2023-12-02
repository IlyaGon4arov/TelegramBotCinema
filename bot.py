import telebot
import json
import parsing


with open("data.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)
    TOKEN = json_data["TOKEN"] # Get token from data.json


bot = telebot.TeleBot(TOKEN) # set bot
city = None

markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True) # set buttons
button1 = telebot.types.KeyboardButton("У прокаті")
button2 = telebot.types.KeyboardButton("Скоро будуть")
markup.add(button1, button2)


@bot.message_handler(commands=["start"]) # what programm doing when there is command "start"
def welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = telebot.types.KeyboardButton("/city")
    markup.add(button)
    bot.send_message(message.chat.id, "⚡ Привіт! Я бот, який створений для того, щоб зручно переглядати наявність фільмів у кінопрокаті. ⚡\nЯ спираюсь на дані сайту www.wizoria.ua")
    bot.send_message(message.chat.id, "Спочатку давай оберем місце, за яким тобі буде зручно слідкувати. Обери один із запропонованих нижче варіантів!", reply_markup=markup)


@bot.message_handler(commands=["city"]) # what programm doing when there is command "city"
def choose_city(message):
    all_cities = parsing.get_cities()
    markup = telebot.types.InlineKeyboardMarkup()
    for key in all_cities:
        button = telebot.types.InlineKeyboardButton(key, callback_data=f"city-{all_cities[key]}-{key}")
        markup.add(button)
    bot.send_message(message.chat.id, "Будь ласка, оберіть місто із запропонованих", reply_markup=markup)


@bot.callback_query_handler(func = lambda callback: True) # set city
def callback_message(callback):
    callback_arr = callback.data.split("-")
    if callback_arr[0] == 'city':
        global city
        city = callback_arr[1]
        bot.send_message(callback.from_user.id, f"Вітаю, Ви обрали {callback_arr[2]}!", reply_markup=markup)


@bot.message_handler()
def give_data(message):
    if city is None:
        markup_city = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = telebot.types.KeyboardButton("/city")
        markup_city.add(button)
        bot.send_message(message.chat.id, "Будь ласка, оберіть місто", reply_markup=markup_city)
    else:
        match message.text:
            case "У прокаті": # what programm doing when there is message "У проакті"
                movies = parsing.get_movies(request_type="current", city_href=city)
                for item in movies:
                    mess_text = f"Назва фільму: {item['title']}\nВікове обмеження: {item['age']}\nЖанри: {item['genres']}\n{item['href']}"
                    bot.send_message(message.chat.id, mess_text, reply_markup=markup)
            case "Скоро будуть": # what programm doing when there is message "Скоро будуть"
                movies = parsing.get_movies(request_type="comming_soon", city_href=city)
                for item in movies:
                    mess_text = f"Назва фільму: {item['title']}\nВікове обмеження: {item['age']}\nЖанри: {item['genres']}\nДата прем'єри: {item['premiere_date']}"
                    if item["description"] is not None:
                        mess_text += f"\nОпис фільму: {item['description']}"
                    mess_text += f"\n{item['href']}"
                    bot.send_message(message.chat.id, mess_text, reply_markup=markup)


bot.polling(none_stop=True)

