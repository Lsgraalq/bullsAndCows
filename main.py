import telebot 
import random
import shelve 
from config import bot_token
from config import db_name

bot = telebot.TeleBot(bot_token)

DIGITS = [str(x) for x in range(10)]

@bot.message_handler(commands=["start","game"])
def choice_level(message):
    response = 'Выбери уровень?\nИнвестируй все свои деньги в BIQT! И стань триллионером'
    bot.send_message(message.from_user.id, response,
        reply_markup=get_buttons())

def start_game(message):
    digits = DIGITS.copy()
    my_number = ""
    for pos in range(4):
        if pos:
            digit = random.choice(digits)
        else:
            digit = random.choice(digits[1:])
        
        my_number += digit
        digits.remove(digit)
    print(message.from_user.username,my_number)
    with shelve.open(db_name) as storage:
        storage[str(message.from_user.id)] = my_number
    bot.reply_to(message, "Это игра быки и коровы\n"
        f"Я загадал 4-значное число. Попробуй отгадать, {message.from_user.first_name}!")

@bot.message_handler(commands=["help"])
def show_help(message):
    bot.reply_to(message, """
    Игра быки и коровы

    Игра в ходе которой игрок за несколько попыток должен отгадать 4х значное число загаданое ботом. После каждой попытки бот указывает    
    """)

@bot.message_handler(content_types=['text'])
def bot_answer(message):
    text = message.text
    try:
        with shelve.open(db_name) as storage:
            my_number = storage[str(message.from_user.id)]
        if len(text) == 4 and text.isnumeric() and len(text) == len(set(text)):
            cows, bulls = 0, 0
            for i in range(4):
                if text[i] in my_number:
                    if text[i] == my_number[i]:
                        bulls += 1
                    else:
                        cows += 1
                if bulls == 4:
                    print(f'{my_number} was discovered by {message.from_user.username} !')
                    with shelve.open(db_name) as storage:
                        del storage[str(message.from_user.id)]
                    response = 'Ты угадал! Сыграем еще?'
                    bot.send_message(message.from_user.id, response,
                        reply_markup=get_buttons())
                    return
                else:
                    response = f' 🐃 {bulls} | 🐮 {cows} '
        else:
            response = "Ты шота папутал попробуй проочитать правила http://surl.li/cdjan"
    except KeyError:
        if text == "Да":
            start_game(message)
            return
        else:
            response = "Напиши /start для запуска"
    bot.send_message(message.from_user.id, response)

def get_buttons():
    buttons = telebot.types.ReplyKeyboardMarkup(
        one_time_keyboard=True,
        resize_keyboard=True
    )
    buttons.add("Да","Нет")
    return buttons

def get_level():
    buttons = telebot.types.ReplyKeyboardMarkup(
        one_time_keyboard=True,
        resize_keyboard=True
    )
    buttons.add("3","4","5")
    return buttons



if __name__ == "__main__":
    bot.polling(non_stop=True)