import telebot 
import random
from config import bot_token

bot = telebot.TeleBot(bot_token)

DIGITS = [str(x) for x in range(10)]
my_number=""
active_game = False

@bot.message_handler(commands=["start","game"])
def start_game(message):
    digits = DIGITS.copy()
    global my_number , active_game
    my_number = ""
    for pos in range(4):
        if pos:
            digit = random.choice(digits)
        else:
            digit = random.choice(digits[1:])
        
        my_number += digit
        digits.remove(digit)
    print(message.from_user.first_name,my_number)
    active_game = True
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
    global active_game
    text = message.text
    if not active_game:
        if text == "Да":
            start_game(message)
            return
        else:
            bot.send_message("Напиши /start для запуска")
    if len(text) == 4 and text.isnumeric() and len(text) == len(set(text)):
        cows, bulls = 0, 0
        for i in range(4):
            if text[i] in my_number:
                if text[i] == my_number[i]:
                    bulls += 1
                else:
                    cows += 1
        if bulls == 4:
            response = "ура,п0беда! Сыграем еще?" 
            active_game = False
            bot.send_message(message.from_user.id, response, 
                reply_markup=get_buttons())
            return
        else:
            response = f' 🐃 {bulls} | 🐮 {cows} '
    else:
        response = "Ты шота папутал попробуй проочитать правила http://surl.li/cdjan"
    bot.send_message(message.from_user.id, response)

def get_buttons():
    buttons = telebot.types.ReplyKeyboardMarkup(
        one_time_keyboard=True,
        resize_keyboard=True
    )
    buttons.add("Да","Нет")
    return buttons

if __name__ == "__main__":
    bot.polling(non_stop=True)