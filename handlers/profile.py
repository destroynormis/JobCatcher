from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from models.profile_state import ProfileForm
from keyboards.keyboards import confirm_keyboard

router = Router()


@router.message(ProfileForm.name)
async def get_name(message: Message, state: FSMContext):

    data = await state.get_data()
    profile = data.get("profile", {})

    profile["name"] = message.text

    await state.update_data(profile=profile)

    await message.answer("🎂 Сколько тебе лет?")

    await state.set_state(ProfileForm.age)


@router.message(ProfileForm.age)
async def get_age(message: Message, state: FSMContext):

    data = await state.get_data()
    profile = data.get("profile")

    profile["age"] = message.text

    await state.update_data(profile=profile)

    await message.answer(
        "🛠 Напиши свои навыки через запятую\n"
        "Например: Python, SQL, Django"
    )

    await state.set_state(ProfileForm.skills)


@router.message(ProfileForm.skills)
async def get_skills(message: Message, state: FSMContext):

    data = await state.get_data()
    profile = data.get("profile")

    skills = [s.strip() for s in message.text.split(",")]

    profile["skills"] = skills

    await state.update_data(profile=profile)

    await message.answer("📈 Какой у тебя опыт в IT?")

    await state.set_state(ProfileForm.experience)


@router.message(ProfileForm.experience)
async def get_experience(message: Message, state: FSMContext):

    data = await state.get_data()
    profile = data.get("profile")

    profile["experience"] = message.text

    await state.update_data(profile=profile)

    await message.answer("💰 Какую зарплату ты хочешь?")

    await state.set_state(ProfileForm.salary)


@router.message(ProfileForm.salary)
async def get_salary(message: Message, state: FSMContext):

    data = await state.get_data()
    profile = data.get("profile")

    profile["salary"] = message.text

    await state.update_data(profile=profile)

    resume = f"""
🎉 <b>ТВОЁ РЕЗЮМЕ</b>

👤 {profile['name']}
🎂 {profile['age']}

🛠 {", ".join(profile['skills'])}

📈 {profile['experience']}

💰 {profile['salary']}
"""

    await message.answer(resume, reply_markup=confirm_keyboard())

    await state.set_state(ProfileForm.confirm)