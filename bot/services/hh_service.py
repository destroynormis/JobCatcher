import aiohttp

HEADERS = {"User-Agent": "JobCatcherBot/2.0 (твоя_почта@gmail.com)"}


async def get_area_id(city_name: str) -> str | None:
    """Превращает название города в ID региона на HH.ru"""
    if not city_name or city_name.lower() in ["любой", "удаленка", "любой / удаленка", "нет", "везде"]:
        return None

    url = "https://api.hh.ru/suggests/areas"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(url, params={"text": city_name}) as response:
            if response.status == 200:
                data = await response.json()
                items = data.get("items", [])
                if items:
                    return items[0]["id"]  # Берем точный ID первого совпадения
    return None


async def search_vacancies(search_params: dict) -> list:
    url = "https://api.hh.ru/vacancies"

    # Базовые параметры
    payload = {
        "text": search_params.get("text", "IT"),
        "per_page": 5,
        "page": 0
    }

    # Строгие фильтры HH.ru
    if search_params.get("area"):
        payload["area"] = search_params["area"]
    if search_params.get("experience"):
        payload["experience"] = search_params["experience"]
    if search_params.get("schedule"):
        payload["schedule"] = search_params["schedule"]

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(url, params=payload) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("items", [])
            else:
                print(f"Ошибка HH API: {response.status} - {await response.text()}")
                return []