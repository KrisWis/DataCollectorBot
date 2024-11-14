from utils import text
from aiogram.filters import Filter
from aiogram import types
from aiogram.fsm.context import FSMContext

# Фильтр для определения у юзера наличия юзернейма
class UsernameIsRequiredFilter(Filter):
    async def __call__(self, message: types.Message, state: FSMContext) -> bool:
        username = message.from_user.username

        if not username:
            await message.answer(text.username_is_required_text)

            return False

        return True