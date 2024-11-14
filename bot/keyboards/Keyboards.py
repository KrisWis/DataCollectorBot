from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Клавиатура стартового меню
def start_menu_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🗂 Получить методичку', callback_data='start|get_methodology')],
    [InlineKeyboardButton(text='📤 Отправить данные на анализ', callback_data='start|send_data')],
    [InlineKeyboardButton(text='❓ Задать вопрос менеджеру', callback_data='start|ask_question')]])

    return kb