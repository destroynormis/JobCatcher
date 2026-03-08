import json
import re

def clean_and_parse_json(gpt_response: str) -> dict:
    """Очищает ответ GPT от Markdown и возвращает словарь."""
    cleaned = re.sub(r"```(?:json)?\s*(.*?)\s*```", r"\1", gpt_response, flags=re.DOTALL)
    try:
        return json.loads(cleaned.strip())
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга Yandex GPT: {e}\nТекст был: {gpt_response}")
        return {"text": "IT"} # Безопасный фоллбэк