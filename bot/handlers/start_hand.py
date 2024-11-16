from aiogram import types, F
from InstanceBot import router
from aiogram.filters import StateFilter
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
from filters import MainMenuFilter


# Отправка стартового меню при вводе "/start"
async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    now = datetime.datetime.now()

    if not await AsyncORM.get_user(user_id):

        await AsyncORM.add_user(
            user_id,
            now,
            message.from_user.language_code,
        )

        user_info = {
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "id": message.from_user.id,
            "is_premium": message.from_user.is_premium,
            "language_code": message.from_user.language_code,
        }

        await message.answer(text.start_text, reply_markup=Keyboards.redirect_to_start_menu_kb())
    
        await bot.send_message(os.getenv("MANAGER_GROUP_ID"), 
                    text.start_user_info_text.format(
                    f"@{user_info["username"]}" if user_info["username"] else '"Юзернейм отсутствует"', 
                    user_info["first_name"] if user_info["first_name"] else "❌", 
                    user_info["last_name"] if user_info["last_name"] else "❌", user_info["id"],
                    "✅" if user_info["is_premium"] else "❌",
                    user_info["language_code"] if user_info["language_code"] else "❌"))


    await message.answer(text.start_menu_text, reply_markup=Keyboards.start_menu_kb())
    await state.clear()


# Отправка сообщения, чтобы пользователь отправил свой номер телефона
async def wait_user_phoneNumber(message: types.Message, state: FSMContext):

    name = message.text

    if name:

        await state.update_data(name=name)
        
        await message.answer(text.send_your_phoneNumber_text)

        await state.set_state(UserStates.write_phoneNumber)
    else:
        message.answer(text.data_is_invalid_text)

# Когда юзер отправил номер телефона, при анализе
async def send_end_message_of_analyz(message: types.Message, state: FSMContext):

    user_phoneNumber = message.text

    data = await state.get_data()

    if "user_name" in data:
        user_name = data["user_name"]
    else:
        user_name = f"@{message.from_user.username}"

    name = data["name"]

    user_text_arr_text = ""

    if "user_text_arr" in data:
        if len(data["user_text_arr"]):
            user_text_arr_text = "\n\n".join([text for text in data["user_text_arr"] if text is not None and text != ""])
    
    try:
        if carrier._is_mobile(number_type(phonenumbers.parse(user_phoneNumber))):

            user_info = {
                "user_name": user_name,
                "first_name": message.from_user.first_name,
                "last_name": message.from_user.last_name,
                "id": message.from_user.id,
                "is_premium": message.from_user.is_premium,
                "language_code": message.from_user.language_code,
            }

            if "photo_file_ids" in data:
                photo_file_ids = data["photo_file_ids"]
            else:
                photo_file_ids = []

            if "video_file_ids" in data:
                video_file_ids = data["video_file_ids"]
            else:
                video_file_ids = []

            if "audio_file_ids" in data:
                audio_file_ids = data["audio_file_ids"]
            else:
                audio_file_ids = []

            if "document_file_ids" in data:
                document_file_ids = data["document_file_ids"]
            else:
                document_file_ids = []

            if sum([len(photo_file_ids), len(video_file_ids), len(audio_file_ids), len(document_file_ids)]) > 1 or len(photo_file_ids) > 1 or len(video_file_ids) > 1 or len(audio_file_ids) > 1 or len(document_file_ids) > 1:
                media_group_elements = []

                for photo_file_id in photo_file_ids:
                    media_group_elements.append(types.InputMediaPhoto(media=photo_file_id))

                for video_file_id in video_file_ids:
                    media_group_elements.append(types.InputMediaVideo(media=video_file_id))

                for audio_file_id in audio_file_ids:
                    await bot.send_audio(os.getenv("MANAGER_GROUP_ID"), audio=audio_file_id)
                
                for document_file_id in document_file_ids:
                    await bot.send_document(os.getenv("MANAGER_GROUP_ID"), document=document_file_id)

                if len(media_group_elements):
                    try:
                        await bot.send_media_group(os.getenv("MANAGER_GROUP_ID"), media_group_elements)
                    except:
                        media_group_elements_arr = []

                        for index in range(0, len(media_group_elements), 10):
                            media_group_elements_arr.append(media_group_elements[index: index + 10])

                        for media_group_element in media_group_elements_arr:
                            await bot.send_media_group(os.getenv("MANAGER_GROUP_ID"), media_group_element)
                    
                    if user_text_arr_text:
                        await bot.send_message(os.getenv("MANAGER_GROUP_ID"), 
                                        text.send_data_for_analyz_to_manager_mediagroup_text.
                                        format(user_info["user_name"],
                            user_info["id"], name, user_phoneNumber,
                            user_info["last_name"] if user_info["last_name"] else "❌",
                            "✅" if user_info["is_premium"] else "❌",
                            user_info["language_code"] if user_info["language_code"] else "❌",
                            user_text_arr_text))
                    else:
                        await bot.send_message(os.getenv("MANAGER_GROUP_ID"), 
                                        text.send_data_for_analyz_to_manager_mediagroup_without_text_text.
                                        format(user_info["user_name"],
                            user_info["id"], name, user_phoneNumber,
                            user_info["last_name"] if user_info["last_name"] else "❌",
                            "✅" if user_info["is_premium"] else "❌",
                            user_info["language_code"] if user_info["language_code"] else "❌"))

            elif len(photo_file_ids):
                if user_text_arr_text:
                    await bot.send_photo(os.getenv("MANAGER_GROUP_ID"), photo=photo_file_ids[0], 
                                    caption=text.send_data_for_analyz_to_manager_with_images_with_text.
                                    format(user_info["user_name"],
                        user_info["id"], name, user_phoneNumber,
                        user_info["last_name"] if user_info["last_name"] else "❌",
                        "✅" if user_info["is_premium"] else "❌",
                        user_info["language_code"] if user_info["language_code"] else "❌",
                        user_text_arr_text))
                else:
                    await bot.send_photo(os.getenv("MANAGER_GROUP_ID"), photo=photo_file_ids[0], 
                                    caption=text.send_data_for_analyz_to_manager_with_images_without_text.
                                    format(user_info["user_name"],
                        user_info["id"], name, user_phoneNumber,
                        user_info["last_name"] if user_info["last_name"] else "❌",
                        "✅" if user_info["is_premium"] else "❌",
                        user_info["language_code"] if user_info["language_code"] else "❌"))
                    
            elif len(video_file_ids):
                if user_text_arr_text:
                    await bot.send_video(os.getenv("MANAGER_GROUP_ID"), video=video_file_ids[0], 
                                    caption=text.send_data_for_analyz_to_manager_with_images_with_text.
                                    format(user_info["user_name"],
                        user_info["id"], name, user_phoneNumber,
                        user_info["last_name"] if user_info["last_name"] else "❌",
                        "✅" if user_info["is_premium"] else "❌",
                        user_info["language_code"] if user_info["language_code"] else "❌",
                        user_text_arr_text))
                else:
                    await bot.send_video(os.getenv("MANAGER_GROUP_ID"), video=video_file_ids[0], 
                                    caption=text.send_data_for_analyz_to_manager_with_images_without_text.
                                    format(user_info["user_name"],
                        user_info["id"], name, user_phoneNumber,
                        user_info["last_name"] if user_info["last_name"] else "❌",
                        "✅" if user_info["is_premium"] else "❌",
                        user_info["language_code"] if user_info["language_code"] else "❌"))
                    
            elif len(audio_file_ids):
                if user_text_arr_text:
                    await bot.send_audio(os.getenv("MANAGER_GROUP_ID"), audio=audio_file_ids[0], 
                                    caption=text.send_data_for_analyz_to_manager_with_images_with_text.
                                    format(user_info["user_name"],
                        user_info["id"], name, user_phoneNumber,
                        user_info["last_name"] if user_info["last_name"] else "❌",
                        "✅" if user_info["is_premium"] else "❌",
                        user_info["language_code"] if user_info["language_code"] else "❌",
                        user_text_arr_text))
                else:
                    await bot.send_audio(os.getenv("MANAGER_GROUP_ID"), audio=audio_file_ids[0], 
                                    caption=text.send_data_for_analyz_to_manager_with_images_without_text.
                                    format(user_info["user_name"],
                        user_info["id"], name, user_phoneNumber,
                        user_info["last_name"] if user_info["last_name"] else "❌",
                        "✅" if user_info["is_premium"] else "❌",
                        user_info["language_code"] if user_info["language_code"] else "❌"))
                    
            elif len(document_file_ids):
                if user_text_arr_text:
                    await bot.send_document(os.getenv("MANAGER_GROUP_ID"), document=document_file_ids[0], 
                                    caption=text.send_data_for_analyz_to_manager_with_images_with_text.
                                    format(user_info["user_name"],
                        user_info["id"], name, user_phoneNumber,
                        user_info["last_name"] if user_info["last_name"] else "❌",
                        "✅" if user_info["is_premium"] else "❌",
                        user_info["language_code"] if user_info["language_code"] else "❌",
                        user_text_arr_text))
                else:
                    await bot.send_document(os.getenv("MANAGER_GROUP_ID"), document=document_file_ids[0], 
                                    caption=text.send_data_for_analyz_to_manager_with_images_without_text.
                                    format(user_info["user_name"],
                        user_info["id"], name, user_phoneNumber,
                        user_info["last_name"] if user_info["last_name"] else "❌",
                        "✅" if user_info["is_premium"] else "❌",
                        user_info["language_code"] if user_info["language_code"] else "❌"))

            else:
                await bot.send_message(os.getenv("MANAGER_GROUP_ID"), 
                    text.send_data_for_analyz_to_manager_text.format(user_info["user_name"],
                        user_info["id"], name, user_phoneNumber,
                        user_info["last_name"] if user_info["last_name"] else "❌",
                        "✅" if user_info["is_premium"] else "❌",
                        user_info["language_code"] if user_info["language_code"] else "❌",
                        user_text_arr_text))
                
            await message.answer(text.send_data_for_analyz_success_text, reply_markup=Keyboards.back_to_start_menu_kb())
            
            await state.clear()
            
            return
        
    except Exception as e: logger.info(e)

    await message.answer(text.your_phoneNumber_is_invalid_text)


# Отправка pdf-файла пользователю
async def send_pdf_file(message: types.Message, state: FSMContext):

    name = message.text

    if name:

        data = await state.get_data()

        if "user_name" in data:
            username = data["user_name"]
        else:
            username = f"@{message.from_user.username}"

        user_id = message.from_user.id
                
        await message.answer(text.send_pdf_file_text, reply_markup=Keyboards.back_to_start_menu_kb())

        await bot.send_message(os.getenv("MANAGER_GROUP_ID"), 
                    text.send_contact_data_to_manager_text.format(username, user_id, name))
        
        await state.clear()

    else:
        message.answer(text.data_is_invalid_text)


# Отправка сообщения о том, что отчёты будут поступать
async def send_message_about_reports(message: types.Message, state: FSMContext):

    name = message.text

    if name:

        data = await state.get_data()

        if "user_name" in data:
            username = data["user_name"]
        else:
            username = f"@{message.from_user.username}"

        user_info = {
            "user_name": username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "id": message.from_user.id,
            "is_premium": message.from_user.is_premium,
            "language_code": message.from_user.language_code,
        }

        now = datetime.datetime.now()

        current_month_name = now.strftime("%B")

        current_month_text = "января"
        
        if current_month_name in ["January", "February", "March"]:
            current_month_text = "апреля"

        elif current_month_name in ["April", "May", "June"]:
            current_month_text = "июля"

        elif current_month_name in ["July", "August", "September"]:
            current_month_text = "октября"
        
        await message.answer(text.send_data_to_manager_for_reports_success_text.format(current_month_text), reply_markup=Keyboards.back_to_start_menu_kb())

        await bot.send_message(os.getenv("MANAGER_GROUP_ID"), 
                    text.send_data_to_manager_for_reports_text.
                    format(username,
                            user_info["id"], name,
                            user_info["last_name"] if user_info["last_name"] else "❌",
                            "✅" if user_info["is_premium"] else "❌",
                            user_info["language_code"] if user_info["language_code"] else "❌"))
        
        await state.clear()
    else:
        message.answer(text.data_is_invalid_text)

# Отправка данных, введённых пользователем, на анализ менеджеру
async def send_data_for_analyz(message: types.Message, state: FSMContext):
    data = await state.get_data()

    user_text = message.text or message.caption
    
    if "user_text_arr" in data:
        user_text_arr = data["user_text_arr"]
    else:
        user_text_arr = []

    user_text_arr.append(user_text)

    await state.update_data(user_text_arr=user_text_arr)

    photo = message.photo
    video = message.video
    document = message.document
    audio = message.audio

    if user_text_arr or photo or video or document or audio:
        if photo: 
            photo = photo[-1]

            if "photo_file_ids" in data:
                photo_file_ids = data["photo_file_ids"]
            else:
                photo_file_ids = []

            photo_file_ids.append(photo.file_id)

            await state.update_data(photo_file_ids=photo_file_ids)

        if video: 

            if "video_file_ids" in data:
                video_file_ids = data["video_file_ids"]
            else:
                video_file_ids = []

            video_file_ids.append(video.file_id)

            await state.update_data(video_file_ids=video_file_ids)

        if document: 
            if "document_file_ids" in data:
                document_file_ids = data["document_file_ids"]
            else:
                document_file_ids = []

            document_file_ids.append(document.file_id)

            await state.update_data(document_file_ids=document_file_ids)

        if audio: 
            if "audio_file_ids" in data:
                audio_file_ids = data["audio_file_ids"]
            else:
                audio_file_ids = []

            audio_file_ids.append(audio.file_id)

            await state.update_data(audio_file_ids=audio_file_ids)

        current_state = await state.get_state()
        if current_state == UserStates.write_data_for_analyz:
            await state.set_state(None)
            await message.answer(text.send_data_for_analyz_continue_text, reply_markup=Keyboards.continue_send_data_kb())
    else:
        await message.answer(text.data_is_invalid_text)


# Отправка юзернейма пользователем при анализе
async def send_username_by_user_for_analyze(message: types.Message, state: FSMContext):

    user_name = message.text

    if user_name.startswith("@"):

        await state.update_data(user_name=user_name)

        await message.answer(text.send_your_name_with_username_text)

        await state.set_state(UserStates.write_name_for_analyz)
    else:
        await message.answer(text.data_is_invalid_text)


# Отправка юзернейма пользователем при получении методички
async def send_username_by_user_for_methodology(message: types.Message, state: FSMContext):

    user_name = message.text

    if user_name.startswith("@"):

        await state.update_data(user_name=user_name)

        await message.answer(text.send_your_name_with_username_text)

        await state.set_state(UserStates.write_name)
    else:
        await message.answer(text.data_is_invalid_text)


# Отправка юзернейма пользователем при получении отчётов
async def send_username_by_user_for_reports(message: types.Message, state: FSMContext):

    user_name = message.text

    if user_name.startswith("@"):

        await state.update_data(user_name=user_name)

        await message.answer(text.send_your_name_with_username_text)

        await state.set_state(UserStates.write_name_for_reports)
    else:
        await message.answer(text.data_is_invalid_text)


# Отправка юзернейма пользователем при задавании вопроса
async def send_username_by_user_for_question(message: types.Message, state: FSMContext):

    user_name = message.text

    if user_name.startswith("@"):

        await state.update_data(user_name=user_name)

        await message.answer(text.send_your_question_text)

        await state.set_state(UserStates.write_question)
    else:
        await message.answer(text.data_is_invalid_text)


# Отправка данных, введённых пользователем, на анализ менеджеру (ДЛЯ МЕДИАГРУПП)
async def send_data_mediagroup_for_analyz(message: types.Message, album: List[types.Message], state: FSMContext):
    user_text = ""

    for element in album:
        data = await state.get_data()

        if element.caption:
            user_text = element.caption

        try:
            if element.photo: 
                photo = element.photo[-1]

                if "photo_file_ids" in data:
                    photo_file_ids = data["photo_file_ids"]
                else:
                    photo_file_ids = []

                photo_file_ids.append(photo.file_id)

                await state.update_data(photo_file_ids=photo_file_ids)

            elif element.video: 

                if "video_file_ids" in data:
                    video_file_ids = data["video_file_ids"]
                else:
                    video_file_ids = []

                video_file_ids.append(element.video.file_id)

                await state.update_data(video_file_ids=video_file_ids)

            elif element.document: 
                if "document_file_ids" in data:
                    document_file_ids = data["document_file_ids"]
                else:
                    document_file_ids = []

                document_file_ids.append(element.document.file_id)

                await state.update_data(document_file_ids=document_file_ids)

            elif element.audio: 
                if "audio_file_ids" in data:
                    audio_file_ids = data["audio_file_ids"]
                else:
                    audio_file_ids = []

                audio_file_ids.append(element.audio.file_id)

                await state.update_data(audio_file_ids=audio_file_ids)
            else:
                return message.answer(text.data_is_invalid_text)
        except Exception as e:
            logger.info(e)
            await message.answer(text.send_data_for_analyz_to_manager_formatError_text)
    
    if "user_text_arr" in data:
        user_text_arr = data["user_text_arr"]
    else:
        user_text_arr = []

    user_text_arr.append(user_text)
    await state.update_data(user_text_arr=user_text_arr)

    current_state = await state.get_state()
    if current_state == UserStates.write_data_for_analyz:
        await state.set_state(None)
        await message.answer(text.send_data_for_analyz_continue_text, reply_markup=Keyboards.continue_send_data_kb())          


# Отправка dвопроса пользователя менеджеру
async def send_user_question(message: types.Message, state: FSMContext):

    user_question = message.text

    data = await state.get_data()

    if "user_name" in data:
        username = data["user_name"]
    else:
        username = f"@{message.from_user.username}"
        
    user_id = message.from_user.id

    await bot.send_message(os.getenv("MANAGER_GROUP_ID"), 
                text.send_user_question_to_manager_text.format(username, user_id, user_question))
    
    await message.answer(text.send_user_question_to_manager_success_text, reply_markup=Keyboards.back_to_start_menu_kb())
    
    await state.clear()


def hand_add():
    router.message.register(start, StateFilter("*"), MainMenuFilter())

    router.message.register(send_username_by_user_for_analyze, StateFilter(UserStates.write_username_for_analyz))

    router.message.register(send_username_by_user_for_methodology, StateFilter(UserStates.write_username))

    router.message.register(send_username_by_user_for_reports, StateFilter(UserStates.write_username_for_reports))

    router.message.register(send_username_by_user_for_question, StateFilter(UserStates.write_username_for_question))

    router.message.register(send_message_about_reports, StateFilter(UserStates.write_name_for_reports))

    router.message.register(send_pdf_file, StateFilter(UserStates.write_name))

    router.message.register(wait_user_phoneNumber, StateFilter(UserStates.write_name_for_analyz))

    router.message.register(send_data_mediagroup_for_analyz, StateFilter(UserStates.write_data_for_analyz), F.media_group_id)

    router.message.register(send_data_for_analyz, StateFilter(UserStates.write_data_for_analyz))

    router.message.register(send_end_message_of_analyz, StateFilter(UserStates.write_phoneNumber))

    router.message.register(send_user_question, StateFilter(UserStates.write_question))
