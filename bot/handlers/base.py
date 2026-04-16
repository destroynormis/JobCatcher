from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.models.states import JobSearchState # Твои стейты

router = Router()

# ==========================================
# 🔧 ВСПОМОГАТЕЛЬНЫЕ КЛАВИАТУРЫ (Для этого файла)
# В идеале их потом лучше вынести в отдельный файл keyboards.py
# ==========================================
def get_start_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="ПОЕХАЛИ")
    return kb.as_markup(resize_keyboard=True)

def get_main_menu_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="СОЗДАТЬ АНКЕТУ")
    kb.button(text="МОЯ АНКЕТА И ПОРТФОЛИО")
    kb.button(text="ПОЙМАТЬ РАБОТУ")
    kb.button(text="НАСТРОЙКИ ПРИЛОЖЕНИЯ")
    kb.adjust(1) # Кнопки будут идти в столбик, по одной в ряд
    return kb.as_markup(resize_keyboard=True)

def get_back_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="НАЗАД")
    return kb.as_markup(resize_keyboard=True)

# ==========================================
# 🛑 ЭКСТРЕННЫЙ ВЫХОД / КНОПКА НАЗАД (Глобальное правило)
# Этот хендлер стоит вверху и перехватывает эти слова из любого состояния
# ==========================================
@router.message(F.text.lower().in_({"назад", "отменить", "отмена", "в главное меню"}))
@router.message(Command("menu", "cancel"))
async def emergency_exit(message: types.Message, state: FSMContext):
    await state.clear() # Сбрасываем всё, что юзер не дозаполнил
    # Вызываем УЗЕЛ 1
    await message.answer(
        f"Возвращаемся в меню. {message.from_user.first_name}, выберите действие:",
        reply_markup=get_main_menu_kb()
    )

# ==========================================
# 🟢 УЗЕЛ 0: ТОЧКА ВХОДА (/start)
# ==========================================
@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear() # На всякий случай чистим память
    await message.answer(
        "Здравствуйте! Я — ваш личный интеллектуальный помощник для построения карьеры.",
        reply_markup=get_start_kb()
    )

# ==========================================
# 🟡 УЗЕЛ 1: ГЛАВНОЕ МЕНЮ (Реакция на "ПОЕХАЛИ")
# ==========================================
@router.message(F.text == "ПОЕХАЛИ")
async def node_1_main_menu(message: types.Message):
    await message.answer(
        f"Рад знакомству, {message.from_user.first_name}! Что будем делать сегодня?",
        reply_markup=get_main_menu_kb()
    )

# ==========================================
# 🔵 УЗЕЛ 2.1: СОЗДАТЬ АНКЕТУ (Выбор направления)
# ==========================================
@router.message(F.text == "СОЗДАТЬ АНКЕТУ")
async def node_2_1_create_profile(message: types.Message, state: FSMContext):
    await message.answer(
        "Какую должность мы будем рассматривать в новой анкете?\n"
        "*(Например: Старший специалист отдела продаж)*",
        parse_mode="Markdown",
        reply_markup=get_back_kb() # Обязательно даем кнопку НАЗАД!
    )
    # И ВОТ ТОЛЬКО ТЕПЕРЬ мы переводим бота в состояние ожидания профессии!
    await state.set_state(JobSearchState.waiting_for_profession)

# Дальше уже пойдет твой хендлер, который ловит текст профессии
# @router.message(JobSearchState.waiting_for_profession)
# async def node_2_2_smart_interview(...)