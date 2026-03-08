from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.models.states import JobSearchState

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Привет! Я **Job Catcher**.\n\n"
        "Давай найдем работу твоей мечты. Для начала скажи, **какую профессию или должность ты ищешь?**\n"
        "*(Например: Backend разработчик Python)*",
        parse_mode="Markdown"
    )
    # Запускаем шаг 1
    await state.set_state(JobSearchState.waiting_for_profession)