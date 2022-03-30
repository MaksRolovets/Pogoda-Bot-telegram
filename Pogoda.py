import requests
import datetime
import config
import telebot
from random import sample

bot = telebot.TeleBot(config.token_bot)

@bot.message_handler(commands=['start'])
def get_start(message):
    bot.send_message(message.chat.id, 'Привет! Бот умеет следующее:\nПоказывать погоду /pogoda\nГенерировать пароль /newpassword')

@bot.message_handler(commands=['newpassword'])
def get_password(message):

    bot.send_message(message.from_user.id, 'Какой длины вам нужен пароль? (до 62 символов)')
    bot.register_next_step_handler(message, generator_pass)

def generator_pass(message):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    uppers = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '1234567890'
    try:
        lenght = int(message.text)

        string = letters + uppers + numbers

        password = ''.join(sample(string, lenght))

        bot.send_message(message.chat.id, password)
    except:
        bot.send_message(message.chat.id, 'Произошла ошибка, введите длину цифрами и до 62 символов!')
def get_wether(message):

    city = message.text

    pogoda = {
        'drizzle':'Морось \U0001F4A7',
        'clear':"Ясно \U00002600",
        'clouds':'Облачно \U00002601',
        'mist':'Туман \U0001F32B',
        'snow':'Снег \U0001F328',
        'thunderstorm':'Гроза \U000026C8',
        'rain':'Дождь \U0001F327'
    }
    try:
        r1 = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={config.token}')
        data1 = r1.json()
        r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?lat={data1[0]["lat"]}&lon={data1[0]["lon"]}&appid={config.token}&units=metric')
        data = r.json()

        temp = data['main']['temp']
        sky = data['weather'][0]['main']
        if sky.lower() in pogoda:
            sk = pogoda[sky.lower()]
        else:
            sk = 'Выгляни в окно, не пойму что там за погода!'
        wind = data['wind']['speed']
        sinrese = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        sys = sunset - sinrese

        bot.send_message(
            message.chat.id,
            f'***{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}***\n'
            f'\U0001F3D9Город: {city}\n'
            f'\U0001F321Температура: {temp}°C  {sk}\n' 
            f'\U0001F4A8Скорость ветра: {wind} м/с\n'
            f'\U00002600Восход: {sinrese}\n'
            f'\U0001F311Закат: {sunset}\n'
            f'\U0000231BПродолжительность дня: {sys}'
            '***Хорошего дня!***'
        )
    except:
        bot.send_message(message.chat.id, 'Корректно введите город!')

def main(message):
    bot.send_message(message.chat.id, 'Введите город')
    bot.register_next_step_handler(message, get_wether)

@bot.message_handler(commands=['pogoda'])
def use_pogoda(message):
    main(message)

bot.polling()