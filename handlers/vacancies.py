from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from models.profile_state import ProfileForm
from services.hh_service import fetch_hh_vacancies
from handlers.start import cmd_start

router = Router()


@router.message(ProfileForm.confirm, F.text == "🚀 Найти вакансии")
async def show_vacancies(message: Message, state: FSMContext):

    data = await state.get_data()
    profile = data.get("profile")

    vacancies = await fetch_hh_vacancies(profile)

    if not vacancies:
        await message.answer("😢 Вакансии не найдены.")
        return

    for vac in vacancies:

        salary = vac.get("salary")

        if salary:
            salary_str = f"{salary.get('from', '')} {salary.get('currency', '')}"
        else:
            salary_str = "не указана"

        text = (
            f"💼 <b>{vac['name']}</b>\n"
            f"🏢 {vac['employer']['name']}\n"
            f"💰 {salary_str}\n"
            f"{vac['alternate_url']}"
        )

        await message.answer(text)


@router.message(ProfileForm.confirm, F.text == "🔄 Заполнить заново")
async def restart(message: Message, state: FSMContext):
    await cmd_start(message, state)