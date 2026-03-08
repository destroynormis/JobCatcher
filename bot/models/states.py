from aiogram.fsm.state import State, StatesGroup

class JobSearchState(StatesGroup):
    waiting_for_profession = State() # Кого ищем? (Python, Дизайнер)
    waiting_for_city = State()       # Город или Удаленка
    waiting_for_experience = State() # Опыт работы
    waiting_for_schedule = State()   # График (Полный день, удаленка)