from aiogram.fsm.state import State, StatesGroup

# Состояния для пользователя
class UserStates(StatesGroup):
    write_name = State()

    write_phoneNumber = State()