import asyncio
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.models.states import JobSearchState
from bot.services.ai_service import get_search_params_from_gpt
from bot.services.hh_service import search_vacancies, get_area_id
from bot.keyboards import reply

router = Router()


# Шаг 1: Спрашиваем профессию (вызывается после /start из base.py)
@router.message(JobSearchState.waiting_for_profession)
async def process_profession(message: types.Message, state: FSMContext):
    await state.update_data(profession=message.text)
    await state.set_state(JobSearchState.waiting_for_city)
    await message.answer(
        "📍 Отлично! В каком городе ищем работу? (Можешь написать свой или выбрать на клавиатуре)",
        reply_markup=reply.get_city_kb()
    )


# Шаг 2: Спрашиваем город
@router.message(JobSearchState.waiting_for_city)
async def process_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(JobSearchState.waiting_for_experience)
    await message.answer(
        "💼 Сколько у тебя опыта работы в этой сфере?",
        reply_markup=reply.get_experience_kb()
    )


# Шаг 3: Спрашиваем опыт
@router.message(JobSearchState.waiting_for_experience)
async def process_experience(message: types.Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await state.set_state(JobSearchState.waiting_for_schedule)
    await message.answer(
        "⏱ Какой формат работы и график тебя интересует?",
        reply_markup=reply.get_schedule_kb()
    )


# Шаг 4: Финальная обработка
@router.message(JobSearchState.waiting_for_schedule)
async def process_schedule_and_search(message: types.Message, state: FSMContext):
    await state.update_data(schedule=message.text)
    user_data = await state.get_data()

    # Убираем клавиатуру и показываем загрузку
    status_msg = await message.answer(
        "🔥 Все понял! Магия началась...\n"
        "1️⃣ Пробиваю регион по базе\n"
        "2️⃣ Структурирую твои навыки\n"
        "3️⃣ Ищу лучшие совпадения...",
        reply_markup=types.ReplyKeyboardRemove()
    )

    try:
        # 1. Достаем ID города через API HH
        area_id = await get_area_id(user_data['city'])

        # 2. Нейросеть переводит ответы в ключи HH
        search_params = await get_search_params_from_gpt(user_data)

        # 3. Подмешиваем точный ID города к параметрам от нейросети
        if area_id:
            search_params['area'] = area_id

        print(f"ИТОГОВЫЙ ЗАПРОС К HH.RU: {search_params}")

        # 4. Выполняем поиск
        vacancies = await search_vacancies(search_params)

        await status_msg.delete()

        if not vacancies:
            await message.answer("😔 Блин, по таким жестким критериям ничего не нашлось. Давай попробуем чуть шире?")
        else:
            await message.answer(f"🎉 Нашел для тебя горячие вакансии:")

            for vac in vacancies:
                name = vac.get("name", "Без названия")
                employer = vac.get("employer", {}).get("name", "Неизвестная компания")
                salary_data = vac.get("salary")

                if salary_data and salary_data.get("from"):
                    salary = f"от {salary_data['from']} {salary_data['currency']}"
                else:
                    salary = "Зарплата не указана"

                url = vac.get("alternate_url", "")

                text = (
                    f"🔹 <b>{name}</b>\n"
                    f"🏢 {employer}\n"
                    f"💰 {salary}\n"
                    f"🔗 <a href='{url}'>Смотреть и откликнуться</a>"
                )
                await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)
                await asyncio.sleep(0.4)  # Защита от блокировки Telegram

    except Exception as e:
        print(f"Критическая ошибка: {e}")
        await message.answer("❌ Произошла ошибка. Пожалуйста, попробуй еще раз.")

    finally:
        # Зацикливаем бота, чтобы можно было начать заново
        await message.answer("🔄 Хочешь найти что-то еще? Просто напиши мне профессию или должность, которую ищешь!")
        await state.set_state(JobSearchState.waiting_for_profession)