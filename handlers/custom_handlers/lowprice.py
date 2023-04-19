from keyboards.reply.contact import request_contact
from loader import bot
from states.lowprice import UserInfoState
from telebot.types import Message

@bot.message_handler(commands=['lowprice'])
def survey(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)
    bot.send_message(message.from_user.id, f'Привет, {message.from_user.username} введи город')

@bot.message_handler(state=UserInfoState.name)
def get_city(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Спасибо, теперь введи количество отелей')
        bot.set_state(message.from_user.id, UserInfoState.hotels_num, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['сity'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Город может содержать только буквы')
