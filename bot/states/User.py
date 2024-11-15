from aiogram.fsm.state import State, StatesGroup

# Состояния для пользователя
class UserStates(StatesGroup):
    write_name = State()

    write_username = State()

    write_name_for_reports = State()

    write_username_for_reports = State()

    write_username_for_question = State()

    write_phoneNumber = State()

    write_data_for_analyz = State()

    write_question = State()

    write_name_for_analyz = State()

    write_username_for_analyz = State()