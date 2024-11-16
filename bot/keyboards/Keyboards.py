from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

# Клавиатура стартового меню
def start_menu_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Методичку «Выбор управляющего в алготрейдинге»', callback_data='start|get_methodology')],
    [InlineKeyboardButton(text='Анализ вашей трейдинговой стратегии', callback_data='start|send_data')],
    [InlineKeyboardButton(text='Наши квартальные отчёты', callback_data='start|our_reports')],
    [InlineKeyboardButton(text='Наши контакты', callback_data='start|contacts')],
    [InlineKeyboardButton(text='Задать вопрос менеджеру', callback_data='start|ask_question')]])

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


# Клавиатура для продолжения ввода данных для анализа
def continue_send_data_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='continue_send_data|yes'),
    InlineKeyboardButton(text='Нет', callback_data='continue_send_data|no')]])

    return kb


# Клавиатура для проверки ввода данных для анализа
def check_send_data_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Всё ОК', callback_data='continue_send_data|ok'),
    InlineKeyboardButton(text='Добавить данные', callback_data='continue_send_data|yes')]])

    return kb