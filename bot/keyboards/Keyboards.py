from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

# Клавиатура стартового меню
def start_menu_kb(is_admin: bool, crypto_draw_is_turned_on: bool):
    inline_keyboard = []

    if crypto_draw_is_turned_on:
        inline_keyboard.append([InlineKeyboardButton(text='Розыгрыш криптовалюты', callback_data='start|crypto_draw')])

    for button in [
        [InlineKeyboardButton(text='Руководство «Выбор управляющего в алготрейдинге»', callback_data='start|get_methodology')],
        [InlineKeyboardButton(text='Анализ вашей трейдинговой стратегии', callback_data='start|send_data')],
        [InlineKeyboardButton(text='Наши квартальные отчёты', callback_data='start|our_reports')],
        [InlineKeyboardButton(text='Наши контакты', callback_data='start|contacts')],
        [InlineKeyboardButton(text='Задать вопрос менеджеру', callback_data='start|ask_question')]]:
        
        inline_keyboard.append(button)

    if is_admin:
        if crypto_draw_is_turned_on:
            inline_keyboard.append([InlineKeyboardButton(text='🔴 Выключить розыгрыш', callback_data='start|crypto_draw|turn_on')])
        else:
            inline_keyboard.append([InlineKeyboardButton(text='🟢 Включить розыгрыш', callback_data='start|crypto_draw|turn_off')])

    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

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