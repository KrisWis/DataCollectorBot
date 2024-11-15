from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

# Клавиатура стартового меню
def start_menu_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1️⃣ методичку «выбор управляющего в алготрейдинге»', callback_data='start|get_methodology')],
    [InlineKeyboardButton(text='2️⃣ анализ вашей трейдинговой стратегии', callback_data='start|send_data')],
    [InlineKeyboardButton(text='3️⃣ наши квартальные отчёты', callback_data='start|our_reports')],
    [InlineKeyboardButton(text='4️⃣ наши контакты (тг-канал, сайт, контакт для связи)', callback_data='start|contacts')],
    [InlineKeyboardButton(text='5️⃣ задать вопрос менеджеру', callback_data='start|ask_question')]])

    return kb


# Репли-кнопка для перехода в главное меню
def redirect_to_start_menu_kb():
    buttons = [
        [KeyboardButton(text="Главное меню")],
    ]
    kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    return kb


# Инлайн-кнопка для перехода в главное меню
def back_to_start_menu_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='start')]])

    return kb