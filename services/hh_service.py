import aiohttp


async def fetch_hh_vacancies(profile):

    skills = profile.get("skills", [])

    query = " OR ".join(skills)

    url = f"https://api.hh.ru/vacancies?text={query}&per_page=5"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:

            data = await response.json()

    return data.get("items", [])