from keyboards.reply.contact import request_contact
from loader import bot
from states.userinfo import UserInfoState
from telebot.types import Message
import json

@bot.message_handler(commands=['survey'])
def survey(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)
    bot.send_message(message.from_user.id, f'Привет, {message.from_user.username} введи своё имя')

@bot.message_handler(state=UserInfoState.name)
def get_name(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Спасибо, записал. Теперь введи свой возраст')
        bot.set_state(message.from_user.id, UserInfoState.age, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['name'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Имя может содержать только буквы')

@bot.message_handler(state=UserInfoState.age)
def get_age(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Спасибо, записал. Теперь введи страну проживания')
        bot.set_state(message.from_user.id, UserInfoState.country, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['age'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Возраст может быть только числом')

@bot.message_handler(state=UserInfoState.country)
def get_name(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Спасибо, записал. Теперь введи свой город')
    bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['country'] = message.text

@bot.message_handler(state=UserInfoState.city)
def get_city(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Спасибо, записал. Отправь свой номер нажав на кнопку', reply_markup=request_contact())
    bot.set_state(message.from_user.id, UserInfoState.phone_number, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text

@bot.message_handler(content_types=['text', 'contact'], state=UserInfoState.phone_number)
def get_contact(message: Message) -> None:
    if message.content_type == 'contact':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            bot.set_state(message.from_user.id, None, message.chat.id)
            data['phone_number'] = message.contact.phone_number
            text = 'Спасибо за инфу, ваши данные: \n' \
                   f'Имя: {data["name"]}\nВозраст: {data["age"]}\nСтрана: {data["country"]}\nГород: {data["city"]}\nНомер телефона: {data["phone_number"]}'
            bot.send_message(message.from_user.id, text)
        
            with open('data.json', 'a') as f:
                f.write(json.dumps(data))

    else:
        bot.send_message(message.from_user.id, 'Чтобы отправить контактную информацию нажми на кнопку')
