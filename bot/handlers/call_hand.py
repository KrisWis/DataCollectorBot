from aiogram import types
from InstanceBot import router
from states.User import UserStates
from aiogram.fsm.context import FSMContext
from utils import text
from keyboards import Keyboards


# Хендлер после нажатия кнопки "Назад". Отправка сообщения пользователю с главным меню.
async def start(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text.start_menu_text, reply_markup=Keyboards.start_menu_kb())

    await state.set_state(None)


# Хендлер после нажатия кнопки "Получить методичку". Отправка сообщения, чтобы пользователь отправил своё имя.
async def wait_user_name(call: types.CallbackQuery, state: FSMContext):
    username = call.from_user.username

    if username:
        await call.message.answer(text.send_your_name_with_username_text)
        await state.set_state(UserStates.write_name)
    else:
        await call.message.answer(text.send_your_name_without_username_text)
        await state.set_state(UserStates.write_username)


# Хендлер после нажатия кнопки "Отправить данные на анализ". Отправка сообщения, чтобы пользователь отправил данные на анализ.
async def wait_user_data_for_analyz(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text.send_your_data_for_analyz_text)

    await state.set_state(UserStates.write_data_for_analyz)


# Хендлер после нажатия кнопки "Задать вопрос менеджеру". Отправка сообщения, чтобы пользователь написал свой вопрос.
async def wait_user_question(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text.send_your_question_text)

    await state.set_state(UserStates.write_question)


# Хендлер после нажатия кнопки "Наши квартальные отчёты". Отправка сообщения, чтобы пользователь написал своё имя
async def wait_name_for_reports(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text.our_reports_text)

    username = call.from_user.username

    if username:
        await call.message.answer(text.send_your_name_with_username_text)
        await state.set_state(UserStates.write_name_for_reports)
    else:
        await call.message.answer(text.send_your_name_without_username_text)
        await state.set_state(UserStates.write_username_for_reports)


# Хендлер после нажатия кнопки "Наши контакты". Отправка сообщения контактов.
async def our_contacts(call: types.CallbackQuery):
    await call.message.edit_text(text.our_contacts_text, reply_markup=Keyboards.back_to_start_menu_kb())


def hand_add():
    router.callback_query.register(start, lambda call: call.data == "start")

    router.callback_query.register(wait_user_name, lambda call: call.data == "start|get_methodology")

    router.callback_query.register(wait_user_data_for_analyz, lambda call: call.data == "start|send_data")

    router.callback_query.register(wait_user_question, lambda call: call.data == "start|ask_question")

    router.callback_query.register(wait_name_for_reports, lambda call: call.data == "start|our_reports")

    router.callback_query.register(our_contacts, lambda call: call.data == "start|contacts")