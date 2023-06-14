from telebot.handler_backends import State, StatesGroup

#hihprice
# 1. Город
# 2. Количество отелей для вывода
# 3. Необходимо ли вывести фотографии для каждого отеля (ДА или НЕТ)
# 4.        Если ДА то запролсить количество необходимых фотографий(не больше максимума)
# 5.        Если НЕТ то вывести без фотографий

class HighPriceState(StatesGroup):
    city = State()
    hotels_num = State()
    image_status = State()