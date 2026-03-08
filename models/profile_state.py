from aiogram.fsm.state import State, StatesGroup


class ProfileForm(StatesGroup):
    name = State()
    age = State()
    skills = State()
    experience = State()
    salary = State()
    confirm = State()