from aiogram import types
from InstanceBot import router
from states.User import UserStates
from aiogram.fsm.context import FSMContext
from utils import text
from keyboards import Keyboards
from InstanceBot import bot
import os
from database.orm import AsyncORM


# Хендлер после нажатия кнопки "Назад". Отправка сообщения пользователю с главным меню.
async def start(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text.start_menu_text, reply_markup=Keyboards.start_menu_kb())

    await state.clear()


# Хендлер после нажатия кнопки "Получить методичку". Отправка сообщения, чтобы пользователь отправил своё имя.
async def wait_user_name(call: types.CallbackQuery, state: FSMContext):
    username = call.from_user.username

    if username:
        await call.message.edit_text(text.send_your_name_with_username_text)
        await state.set_state(UserStates.write_name)
    else:
        await call.message.edit_text(text.send_your_name_without_username_text)
        await state.set_state(UserStates.write_username)


# Хендлер после нажатия кнопки "Отправить данные на анализ". Отправка сообщения, чтобы пользователь отправил данные на анализ.
async def wait_user_data_for_analyz(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text.send_your_data_for_analyz_text)

    await state.set_state(UserStates.write_data_for_analyz)


# Хендлер после нажатия кнопки "Задать вопрос менеджеру". Отправка сообщения, чтобы пользователь написал свой вопрос.
async def wait_user_question(call: types.CallbackQuery, state: FSMContext):

    username = call.from_user.username

    if username:
        await call.message.edit_text(text.send_your_question_text)
        await state.set_state(UserStates.write_question)
    else:
        await call.message.edit_text(text.send_your_name_without_username_text)
        await state.set_state(UserStates.write_username_for_question)


# Хендлер после нажатия кнопки "Наши квартальные отчёты". Отправка сообщения, чтобы пользователь написал своё имя
async def wait_name_for_reports(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text.our_reports_text)

    username = call.from_user.username

    if username:
        await state.set_state(UserStates.write_name_for_reports)
    else:
        await state.set_state(UserStates.write_username_for_reports)


# Хендлер после нажатия кнопки "Наши контакты". Отправка сообщения контактов.
async def our_contacts(call: types.CallbackQuery):
    await call.message.edit_text(text.our_contacts_text, reply_markup=Keyboards.back_to_start_menu_kb(), disable_web_page_preview=True)
    user_id = call.from_user.id

    user = await AsyncORM.get_user(user_id)

    if not user.user_join_contacts:
        user_info = {
            "username": call.from_user.username,
            "first_name": call.from_user.first_name,
            "last_name": call.from_user.last_name,
            "id": user_id,
            "is_premium": call.from_user.is_premium,
            "language_code": call.from_user.language_code,
        }

        await bot.send_message(os.getenv("MANAGER_GROUP_ID"),
                    text.user_join_contacts_info_text.format(
                    f"@{user_info["username"]}" if user_info["username"] else '"Юзернейм отсутствует"', 
                    user_info["first_name"] if user_info["first_name"] else "❌", 
                    user_info["last_name"] if user_info["last_name"] else "❌", user_info["id"],
                    "✅" if user_info["is_premium"] else "❌",
                    user_info["language_code"] if user_info["language_code"] else "❌"))
        
        await AsyncORM.user_join_contacts(user_id)

# Хендлер после нажатия кнопки "Нет". Отправка сообщения, если пользователь не продолжил ввод для анализа.
async def continue_send_data_no(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(user_id, message_id)
    
    data = await state.get_data()

    user_text_arr_text = ""

    if "user_text_arr" in data:
        if len(data["user_text_arr"]):
            user_text_arr_text = "\n\n".join([text for text in data["user_text_arr"] if text is not None and text != ""])

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
            await call.message.answer_audio(audio=audio_file_id)
        
        for document_file_id in document_file_ids:
            await call.message.answer_document(document=document_file_id)

        if len(media_group_elements):
            try:
                await call.message.answer_media_group(media_group_elements)
            except:
                media_group_elements_arr = []

                for index in range(0, len(media_group_elements), 10):
                    media_group_elements_arr.append(media_group_elements[index: index + 10])

                for media_group_element in media_group_elements_arr:
                    await call.message.answer_media_group(media_group_element, reply_markup=Keyboards.check_send_data_kb())

            if user_text_arr_text:
                await call.message.answer(
                                text.send_data_for_analyz_to_user_mediagroup_text.
                                format(user_text_arr_text), reply_markup=Keyboards.check_send_data_kb())
            else:
                await call.message.answer(
                                text.send_data_for_analyz_to_user_mediagroup_without_text_text, reply_markup=Keyboards.check_send_data_kb())


    elif len(photo_file_ids):
        if user_text_arr_text:
            await call.message.answer_photo(photo=photo_file_ids[0], 
                            caption=text.send_data_for_analyz_to_user_with_images_with_text.
                            format(
                user_text_arr_text), reply_markup=Keyboards.check_send_data_kb())
        else:
            await call.message.answer_photo(photo=photo_file_ids[0], 
                            caption=text.send_data_for_analyz_to_user_with_images_without_text, reply_markup=Keyboards.check_send_data_kb())
            
    elif len(video_file_ids):
        if user_text_arr_text:
            await call.message.answer_video(video=video_file_ids[0], 
                            caption=text.send_data_for_analyz_to_user_with_images_with_text.
                            format(
                user_text_arr_text), reply_markup=Keyboards.check_send_data_kb())
        else:
            await call.message.answer_video(video=video_file_ids[0], 
                            caption=text.send_data_for_analyz_to_user_with_images_without_text, reply_markup=Keyboards.check_send_data_kb())
            
    elif len(audio_file_ids):
        if user_text_arr_text:
            await call.message.answer_audio(audio=audio_file_ids[0], 
                            caption=text.send_data_for_analyz_to_user_with_images_with_text.
                            format(
                user_text_arr_text), reply_markup=Keyboards.check_send_data_kb())
        else:
            await call.message.answer_audio(audio=audio_file_ids[0], 
                            caption=text.send_data_for_analyz_to_user_with_images_without_text, reply_markup=Keyboards.check_send_data_kb())
            
    elif len(document_file_ids):
        if user_text_arr_text:
            await call.message.answer_document(document=document_file_ids[0], 
                            caption=text.send_data_for_analyz_to_user_with_images_with_text.
                            format(
                user_text_arr_text), reply_markup=Keyboards.check_send_data_kb())
        else:
            await call.message.answer_document(document=document_file_ids[0], 
                            caption=text.send_data_for_analyz_to_user_with_images_without_text, reply_markup=Keyboards.check_send_data_kb())

    else:
        await call.message.answer(
            text.send_data_for_analyz_to_user_text.format(
                user_text_arr_text), reply_markup=Keyboards.check_send_data_kb())


# Хендлер после нажатия кнопки "Да". Отправка сообщения, чтобы пользователь продолжил ввод для анализа.
async def continue_send_data_yes(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(user_id, message_id)

    await call.message.answer(text.send_data_for_analyz_continue_yes_text)

    await state.set_state(UserStates.write_data_for_analyz)


# Хендлер после нажатия кнопки "Всё ОК". Отправка сообщения, чтобы пользователю ввёл своё имя.
async def check_send_data_ok(call: types.CallbackQuery, state: FSMContext):
    username = call.from_user.username
    user_id = call.from_user.id
    message_id = call.message.message_id

    await bot.delete_message(user_id, message_id)

    await call.message.answer(text.send_data_for_analyz_to_manager_success_text)
    
    if username:
        await call.message.answer(text.send_your_name_with_username_text)
        await state.set_state(UserStates.write_name_for_analyz)
    else:
        await call.message.answer(text.send_your_name_without_username_text)
        await state.set_state(UserStates.write_username_for_analyz)


def hand_add():
    router.callback_query.register(start, lambda call: call.data == "start")

    router.callback_query.register(wait_user_name, lambda call: call.data == "start|get_methodology")

    router.callback_query.register(wait_user_data_for_analyz, lambda call: call.data == "start|send_data")

    router.callback_query.register(wait_user_question, lambda call: call.data == "start|ask_question")

    router.callback_query.register(wait_name_for_reports, lambda call: call.data == "start|our_reports")

    router.callback_query.register(our_contacts, lambda call: call.data == "start|contacts")

    router.callback_query.register(continue_send_data_no, lambda call: call.data == "continue_send_data|no")

    router.callback_query.register(continue_send_data_yes, lambda call: call.data == "continue_send_data|yes")
    
    router.callback_query.register(check_send_data_ok, lambda call: call.data == "continue_send_data|ok")