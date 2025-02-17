import telebot
from telebot import types
import sqlite3

# Инициализация бота
bot = telebot.TeleBot("7868151791:AAFz7ZWDrXom4GWk6GjHbHis-RkAIrs_x64")

# Подключение к базе данных
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (username TEXT PRIMARY KEY, activations INTEGER, chat_id INTEGER)''')
conn.commit()

# Проверка наличия столбца chat_id
cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()
column_names = [column[1] for column in columns]

if 'chat_id' not in column_names:
    cursor.execute("ALTER TABLE users ADD COLUMN chat_id INTEGER")
    conn.commit()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.username
    chat_id = message.chat.id
    if not username:
        bot.send_message(message.chat.id, "У вас не установлен username. Пожалуйста, установите его в настройках Telegram.")
        return

    # Проверка, есть ли пользователь в базе данных
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (username, activations, chat_id) VALUES (?, 0, ?)", (username, chat_id))
        conn.commit()

    # Создание кнопок с emoji
    markup = types.ReplyKeyboardMarkup(row_width=3)
    item1 = types.KeyboardButton('😀')
    item2 = types.KeyboardButton('😎')
    item3 = types.KeyboardButton('🤖')
    item4 = types.KeyboardButton('🐱')
    item5 = types.KeyboardButton('🚀')
    item6 = types.KeyboardButton('🎉')
    markup.add(item1, item2, item3, item4, item5, item6)

    bot.send_message(message.chat.id, "Выберите верный смайл:", reply_markup=markup)

# Обработчик выбора смайла
@bot.message_handler(func=lambda message: message.text in ['😀', '😎', '🤖', '🐱', '🚀', '🎉'])
def check_emoji(message):
    bot.send_message(message.chat.id, "Правильный выбор! Теперь вы можете использовать основное меню.", reply_markup=types.ReplyKeyboardRemove())
    show_main_menu(message.chat.id)

# Функция для отображения основного меню
def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Наш каталог", callback_data='catalog')
    item2 = types.InlineKeyboardButton("Профиль", callback_data='profile')
    item3 = types.InlineKeyboardButton("Пополнить баланс", callback_data='add_balance')
    markup.add(item1, item2, item3)
    bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)

# Обработчик inline кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'catalog':
        show_catalog(call.message.chat.id)
    elif call.data == 'profile':
        show_profile(call.message.chat.id, call.from_user.username)
    elif call.data == 'add_balance':
        bot.send_message(call.message.chat.id, "Функция пополнения баланса в разработке.")

# Функция для отображения каталога
def show_catalog(chat_id):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Схемы заработка", callback_data='earnings')
    item2 = types.InlineKeyboardButton("Соц сети", callback_data='social')
    item3 = types.InlineKeyboardButton("Seed фразы", callback_data='seed')
    markup.add(item1, item2, item3)
    bot.send_message(chat_id, "Выберите категорию:", reply_markup=markup)

# Функция для отображения профиля
def show_profile(chat_id, username):
    cursor.execute("SELECT activations FROM users WHERE username=?", (username,))
    activations = cursor.fetchone()[0]
    bot.send_message(chat_id, f"Ваш профиль:\nUsername: @{username}\nБаланс: {activations}₽")

# Обработчик команды /актив для админа
@bot.message_handler(commands=['актив'])
def add_activation(message):
    if message.from_user.username == "Qwoxyzz":  # Замените на username админа
        try:
            username = message.text.split()[1]
            usern = int(message.text.split()[2])  # Количество активаций
            cursor.execute("SELECT chat_id FROM users WHERE username=?", (username,))
            user_data = cursor.fetchone()

            if user_data:
                chat_id = user_data[0]
                cursor.execute("UPDATE users SET activations = activations + ? WHERE username=?", (usern, username))
                conn.commit()
                bot.send_message(message.chat.id, f"Активация выдана пользователю @{username} ({usern}₽)")
                # Отправляем уведомление пользователю
                bot.send_message(chat_id, f"Вам была выдана активация на сумму {usern}₽. Ваш баланс пополнен.")
            else:
                bot.send_message(message.chat.id, f"Пользователь @{username} не найден в базе данных.")
        except IndexError:
            bot.send_message(message.chat.id, "Использование: /актив username количество")
        except ValueError:
            bot.send_message(message.chat.id, "Количество активаций должно быть числом.")
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

# Запуск бота
bot.polling(none_stop=True)