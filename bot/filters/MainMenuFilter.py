from aiogram.filters import Filter
from aiogram import types

# Фильтр для определения того, что юзер написал "Главное меню"
class MainMenuFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        if message.text in ["/start", "Главное меню"]:
            return True

        return False