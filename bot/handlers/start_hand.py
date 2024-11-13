from aiogram import types
from InstanceBot import router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext


# Отправка стартового меню при вводе "/start"
async def start(message: types.Message, state: FSMContext):
    await message.answer("Дарова")

    await state.set_state(None)


def hand_add():
    router.message.register(start, StateFilter("*"), CommandStart())
