from aiogram import types
from InstanceBot import router
from states.User import UserStates
from aiogram.fsm.context import FSMContext
from utils import text


# Хендлер после нажатия кнопки "Получить методичку". Отправка сообщения, чтобы пользователь отправил своё имя.
async def wait_user_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text.send_your_name_text)

    await state.set_state(UserStates.write_name)


# Хендлер после нажатия кнопки "Отправить данные на анализ". Отправка сообщения, чтобы пользователь отправил данные на анализ.
async def wait_user_data_for_analyz(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text.send_your_data_for_analyz_text)

    await state.set_state(UserStates.write_data_for_analyz)


# Хендлер после нажатия кнопки "Задать вопрос менеджеру". Отправка сообщения, чтобы пользователь написал свой вопрос.
async def wait_user_question(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text.send_your_question_text)

    await state.set_state(UserStates.write_question)


def hand_add():
    router.callback_query.register(wait_user_name, lambda call: call.data == "start|get_methodology")

    router.callback_query.register(wait_user_data_for_analyz, lambda call: call.data == "start|send_data")

    router.callback_query.register(wait_user_question, lambda call: call.data == "start|ask_question")
