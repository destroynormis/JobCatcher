from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_city_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Москва"), KeyboardButton(text="Санкт-Петербург")],
            [KeyboardButton(text="Любой / Удаленка")]
        ], resize_keyboard=True, one_time_keyboard=True
    )

def get_experience_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Нет опыта"), KeyboardButton(text="От 1 до 3 лет")],[KeyboardButton(text="От 3 до 6 лет"), KeyboardButton(text="Более 6 лет")]
        ], resize_keyboard=True, one_time_keyboard=True
    )

def get_schedule_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Удаленная работа"), KeyboardButton(text="Полный день")],
            [KeyboardButton(text="Гибкий график"), KeyboardButton(text="Сменный график")]
        ], resize_keyboard=True, one_time_keyboard=True
    )