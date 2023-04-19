from telebot.handler_backends import State, StatesGroup

#lowprice
# 1. Город
# 2. Количество отелей для вывода
# 3. Необходимо ли вывести фотографии для каждого отеля (ДА или НЕТ_
# 4.        Если ДА то запролсить количество необходимых фотографий(не больше максимума)
# 5.        Если НЕТ то вывести без фотографий

class UserInfoState(StatesGroup):
    city = State()
    hotels_num = State()
    image_status = State()