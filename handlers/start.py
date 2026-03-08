from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from models.profile_state import ProfileForm

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):

    await state.clear()

    await state.update_data(profile={})

    await message.answer(
        "👋 Привет! Я JobCatcher.\n\n"
        "Давай составим твоё резюме.\n\n"
        "Как тебя зовут?"
    )

    await state.set_state(ProfileForm.name)