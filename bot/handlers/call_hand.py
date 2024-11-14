from aiogram import types
from InstanceBot import router
from states.User import UserStates
from aiogram.fsm.context import FSMContext
from utils import text


# Хендлер после нажатия кнопки "Получить методичку". Отправка сообщения, чтобы пользователь отправил своё имя.
async def wait_user_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text.send_your_name_text)

    await state.set_state(UserStates.write_name)


def hand_add():
    router.callback_query.register(wait_user_name, lambda call: call.data == "start|get_methodology")
