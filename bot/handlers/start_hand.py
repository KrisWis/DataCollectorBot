from aiogram import types
from InstanceBot import router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from utils import text
from keyboards import Keyboards
from states.User import UserStates
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
from RunBot import logger
from InstanceBot import bot
import os


# Отправка стартового меню при вводе "/start"
async def start(message: types.Message, state: FSMContext):
    username = message.from_user.username

    await message.answer(text.start_menu_text.format(username), reply_markup=Keyboards.start_menu_kb())

    await state.set_state(None)


# Отправка сообщения, чтобы пользователь отправил свой номер телефона
async def wait_user_phoneNumber(message: types.Message, state: FSMContext):

    user_name = message.text

    await state.update_data(user_name=user_name)
    
    await message.answer(text.send_your_phoneNumber_text)

    await state.set_state(UserStates.write_phoneNumber)


# Отправка pdf-файла пользователю
async def send_pdf_file(message: types.Message, state: FSMContext):

    user_phoneNumber = message.text

    username = message.from_user.username
    
    try:
        if carrier._is_mobile(number_type(phonenumbers.parse(user_phoneNumber))):
            
            await message.answer_document(document=types.FSInputFile("bot/static/methodology.pdf"), caption=text.send_pdf_file_text)

            data = await state.get_data()

            user_name = data["user_name"]

            await bot.send_message(os.getenv("MANAGER_GROUP_ID"), 
                        text.send_contact_data_to_manager_text.format(username, user_name, user_phoneNumber))
            
            await state.set_state(None)
            
            return
        
    except Exception as e: logger.info(e)

    await message.answer(text.your_phoneNumber_is_invalid_text)


def hand_add():
    router.message.register(start, StateFilter("*"), CommandStart())

    router.message.register(wait_user_phoneNumber, StateFilter(UserStates.write_name))

    router.message.register(send_pdf_file, StateFilter(UserStates.write_phoneNumber))
