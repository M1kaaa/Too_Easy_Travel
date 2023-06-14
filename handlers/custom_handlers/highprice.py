from keyboards.reply.contact import request_contact
from loader import bot
from states.highprice import HighPriceState
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, CallbackQuery
from utils.funcs import get_hotels_ids, get_location_id, get_hotel_detail
import json


@bot.message_handler(commands=['highprice'])
def survey(message: Message) -> None:
    bot.set_state(message.from_user.id, HighPriceState.city, message.chat.id)
    bot.send_message(message.from_user.id,
                     f'Привет, {message.from_user.username} введи город')


@bot.message_handler(state=HighPriceState.city)
def get_city(message: Message) -> None:
    if message.text.isalpha():
        city = message.text
        location_id = get_location_id(city)
        if location_id is not None:
            bot.send_message(message.from_user.id,
                             'Спасибо, теперь введи количество отелей')
            bot.set_state(message.from_user.id,
                          HighPriceState.hotels_num, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['сity'] = message.text
                data['location_id'] = location_id
        else:
            bot.send_message(message.from_user.id,
                             'Город не найден. Введите еще раз')

    else:
        bot.send_message(message.from_user.id,
                         'Город может содержать только буквы')


def image_status_markup():
    destinations = InlineKeyboardMarkup()
    destinations.add(InlineKeyboardButton(
        text='Да', callback_data='image_status:yes'))
    destinations.add(InlineKeyboardButton(
        text='Нет', callback_data='image_status:no'))
    return destinations


@bot.message_handler(state=HighPriceState.hotels_num)
def get_hotels_num(message: Message) -> None:
    if message.text.isnumeric():
        bot.send_message(message.from_user.id,
                         f'Вывести картинки отелей?', reply_markup=image_status_markup())
        bot.set_state(message.from_user.id,
                      HighPriceState.image_status, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['hotels_num'] = int(message.text)
    else:
        bot.send_message(message.from_user.id,
                         'Количество отелей может содержать только цифры')


def send_hotels_info(user_id, chat_id, show_images=False):
    with bot.retrieve_data(user_id, chat_id) as data:
        bot.send_message(user_id, 'Подождите, сейчас загружу информацию')
        location_id = data['location_id']
        count = data['hotels_num']
        sort = 'PRICE_HIGH_TO_LOW'
        hotels_ids = get_hotels_ids(location_id, count, sort='PRICE_HIGH_TO_LOW')
        if hotels_ids is not None:
            hotels = get_hotel_detail(hotels_ids)
            for i, hotel_id in enumerate(hotels_ids, 1):
                hotel = get_hotel_detail(hotel_id)
                answer = (f"\n{i}. {hotel['name']} ({hotel['address']})" +
                          f"\n{hotel['tagline']}")

                if show_images:
                    bot.send_photo(user_id, photo=hotel['image_url'],
                                   caption=answer + '\n' + hotel['image_description'])
                else:
                    bot.send_message(user_id, answer)

        bot.set_state(user_id, None, chat_id)


@bot.callback_query_handler(func=lambda callback_query: callback_query.data.startswith('image_status'))
def set_image_status(callback_query: CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    send_hotels_info(callback_query.from_user.id,
                     callback_query.message.chat.id,
                     ':yes' in callback_query.data)


@bot.message_handler(state=HighPriceState.image_status)
def image_answ(message: Message) -> None:
    send_hotels_info(message.from_user.id, message.chat.id,
                     message.text.lower() == 'да')
