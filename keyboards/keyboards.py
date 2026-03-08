from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def confirm_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚀 Найти вакансии")],
            [KeyboardButton(text="🔄 Заполнить заново")]
        ],
        resize_keyboard=True
    )