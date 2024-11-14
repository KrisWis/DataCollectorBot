from aiogram import types, F
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
from typing import List
from database.orm import AsyncORM
import datetime
from filters.UsernameIsRequiredFilter import UsernameIsRequiredFilter


# Отправка стартового меню при вводе "/start"
async def start(message: types.Message, state: FSMContext):
    username = message.from_user.username
    user_id = message.from_user.id
    now = datetime.datetime.now()

    await message.answer(text.start_menu_text.format(username), reply_markup=Keyboards.start_menu_kb())

    if not await AsyncORM.get_user(user_id):

        await AsyncORM.add_user(
            user_id,
            username,
            now,
            message.from_user.language_code,
        )

        user_info = {
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "id": message.from_user.id,
            "is_premium": message.from_user.is_premium,
            "language_code": message.from_user.language_code,
        }
        
        print(user_info["language_code"] if user_info["language_code"] else "❌")


        await bot.send_message(os.getenv("MANAGER_GROUP_ID"), 
                    text.start_user_info_text.format(username, 
                    user_info["first_name"] if user_info["first_name"] else "❌", 
                    user_info["last_name"] if user_info["last_name"] else "❌", user_info["id"],
                    "✅" if user_info["is_premium"] else "❌",
                    user_info["language_code"] if user_info["language_code"] else "❌"))
    
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
            
            await state.clear()
            
            return
        
    except Exception as e: logger.info(e)

    await message.answer(text.your_phoneNumber_is_invalid_text)


# Отправка данных, введённых пользователем, на анализ менеджеру
async def send_data_for_analyz(message: types.Message, state: FSMContext):
    username = message.from_user.username

    user_text = message.text or message.caption

    photo = message.photo

    if user_text or photo:
        if photo: 
            photo = photo[-1]

            if user_text:
                await bot.send_photo(os.getenv("MANAGER_GROUP_ID"), photo=photo.file_id, 
                                caption=text.send_data_for_analyz_to_manager_text.format(username, user_text))
            else:
                await bot.send_photo(os.getenv("MANAGER_GROUP_ID"), photo=photo.file_id, 
                                caption=text.send_data_for_analyz_to_manager_with_image_without_text.format(username))

        else:
            await bot.send_message(os.getenv("MANAGER_GROUP_ID"), 
                    text.send_data_for_analyz_to_manager_text.format(username, user_text))

        await message.answer(text.send_data_for_analyz_to_manager_success_text)

        await state.clear()

    else:
        await message.answer(text.data_is_invalid_text)


# Отправка данных, введённых пользователем, на анализ менеджеру (ДЛЯ МЕДИАГРУПП)
async def send_data_mediagroup_for_analyz(message: types.Message, album: List[types.Message], state: FSMContext):
    group_elements = []

    username = message.from_user.username

    user_text = message.caption

    for element in album:
        try:
            input_media = types.InputMediaPhoto(media=element.photo[-1].file_id)

            group_elements.append(input_media)
        except:
            await message.answer(text.send_data_for_analyz_to_manager_only_images_text)

    if user_text:
        await bot.send_message(os.getenv("MANAGER_GROUP_ID"), 
                        text.send_data_for_analyz_to_manager_mediagroup_text.format(username, user_text))
    else:
        await bot.send_message(os.getenv("MANAGER_GROUP_ID"), 
                        text.send_data_for_analyz_to_manager_with_images_without_text.format(username))
        
    await bot.send_media_group(os.getenv("MANAGER_GROUP_ID"), group_elements)

    await message.answer(text.send_data_for_analyz_to_manager_success_text)

    await state.clear()


# Отправка dвопроса пользователя менеджеру
async def send_user_question(message: types.Message, state: FSMContext):

    user_question = message.text

    username = message.from_user.username

    await bot.send_message(os.getenv("MANAGER_GROUP_ID"), 
                text.send_user_question_to_manager_text.format(username, user_question))
    
    await message.answer(text.send_user_question_to_manager_success_text)
    
    await state.clear()


def hand_add():
    router.message.register(start, StateFilter("*"), CommandStart(), UsernameIsRequiredFilter())

    router.message.register(wait_user_phoneNumber, StateFilter(UserStates.write_name))

    router.message.register(send_pdf_file, StateFilter(UserStates.write_phoneNumber))

    router.message.register(send_data_mediagroup_for_analyz, StateFilter(UserStates.write_data_for_analyz), F.media_group_id)

    router.message.register(send_data_for_analyz, StateFilter(UserStates.write_data_for_analyz))

    router.message.register(send_user_question, StateFilter(UserStates.write_question))