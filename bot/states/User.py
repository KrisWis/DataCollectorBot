from aiogram.fsm.state import State, StatesGroup

# Состояния для пользователя
class UserStates(StatesGroup):
    write_name = State()

    write_phoneNumber = State()

    write_data_for_analyz = State()

    write_question = State()