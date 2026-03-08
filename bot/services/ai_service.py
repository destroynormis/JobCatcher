import aiohttp
from config import YANDEX_API_KEY, YANDEX_FOLDER_ID
from bot.services.text_cleaner import clean_and_parse_json

# ПРОМПТ С ПРИМЕРАМИ
SYSTEM_PROMPT = """Ты — строгий Senior IT-рекрутер и парсер. Твоя главная задача — ИСПРАВЛЯТЬ кривой пользовательский сленг, опечатки и переводить их в идеальные, стандартизированные поисковые запросы для базы данных HH.ru.
Верни СТРОГО валидный JSON без Markdown, без тегов ```json и без комментариев.

Правила:
1. Ключ "text": НОРМАЛИЗУЙ профессию. 
   - Исправь русский сленг ("Пайтон" -> "Python", "Фронтенд" -> "Frontend Developer").
   - Убери мусорные слова и грейды ("джун", "мидл", "сеньор").
   - ВАЖНО: Если пользователь ищет сразу несколько разных профессий (например, Питон и Джава), соединяй их оператором OR, а не запятыми! Пример: "Python Developer OR Java Developer".
2. Ключ "experience": переведи поле [Опыт] строго в: "noExperience", "between1And3", "between3And6", "moreThan6". 
3. Ключ "schedule": переведи поле[График] строго в: "fullDay", "shift", "flexible", "remote", "flyInFlyOut". Если график не понятен, не пиши этот ключ.
💡 ПРИМЕРЫ ИСПРАВЛЕНИЯ "text":
-[Профессия]: "Пайтон инженер" -> "text": "Python Developer"
-[Профессия]: "хтмл цсс верстальщик" -> "text": "HTML CSS Coder"
-[Профессия]: "дизайнер интерфейсов фигма" -> "text": "UX/UI Designer Figma"
- [Профессия]: "Джаваскрипт мидл" -> "text": "JavaScript Developer"
- [Профессия]: "аналитик данных" -> "text": "Data Analyst"
"""


async def get_search_params_from_gpt(user_data: dict) -> dict:
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
        "x-folder-id": YANDEX_FOLDER_ID
    }

    # Формируем структурированный запрос для GPT
    user_text = (
        f"[Профессия]: {user_data.get('profession')}\n"
        f"[Опыт]: {user_data.get('experience')}\n"
        f"[График]: {user_data.get('schedule')}"
    )

    payload = {
        "modelUri": f"gpt://{YANDEX_FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.1,  # Низкая температура, чтобы ИИ не фантазировал, а работал четко
            "maxTokens": "500"
        },
        "messages": [
            {"role": "system", "text": SYSTEM_PROMPT},
            {"role": "user", "text": user_text}
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                gpt_text = data["result"]["alternatives"][0]["message"]["text"]

                # Добавим принт, чтобы ты видел, как круто ИИ теперь чистит запросы
                print(f"ОТВЕТ ОТ YANDEX GPT:\n{gpt_text}")

                return clean_and_parse_json(gpt_text)
            else:
                print(f"Ошибка API Yandex: {await response.text()}")
            return {"text": "IT"}  # Заглушка на случай падения Yandex