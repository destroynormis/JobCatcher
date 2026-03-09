# Job Catcher

An asynchronous Telegram bot that automates the IT job hunt. Catch your next role before someone else does. Built with Python & Aiogram 3.

## About

JobCatcher collects your professional profile through a natural AI interview (powered by Yandex GPT) and automatically searches for relevant IT vacancies on HH.ru using the official API.

It turns chaotic job hunting into a clean, systematic pipeline: smart profile → targeted search with filters → clean vacancy cards.

## Features

- Natural conversational AI profile builder (Yandex GPT)
- Real-time HH.ru search with official API
- Smart filters: skills, experience level, salary range, location
- Pagination support
- Clean HTML-formatted vacancy output with salary range
- Editable profiles
- Robust error handling (including "query is too old")
- Modular architecture (routers + services + FSM)
- Ready for background notifications and deployment

## Quick Start

1. Clone the repository
   ```bash
   git clone https://github.com/destroynormis/Job_Catcher.git
   cd Job_Catcher
   ```

2. Create and activate virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate    # Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Copy environment template
   ```bash
   cp .env.example .env
   ```
   Fill in your tokens (Telegram Bot Token + Yandex GPT API key).

5. Run the bot
   ```bash
   python -m bot.main
   ```

## Project Structure

```
bot/
├── handlers/     # Telegram routers (vacancies, profile, start, etc.)
├── services/     # hh_service, ai_service
├── keyboards/
├── models/       # FSM states (ProfileForm)
├── utils/
├── main.py
└── config.py
```

## Recent Improvements

- Fixed vacancy text formatting and salary range display
- Enhanced search logic with location constraints and pagination
- Added HH.ru API integration + smart AI dialog flow
- Fixed "query is too old" error
- Prepared for Render deployment

## Roadmap

- [ ] Background vacancy notifications (APScheduler)
- [ ] Persistent storage (PostgreSQL / SQLite + Redis)
- [ ] AI-based vacancy relevance scoring
- [ ] Additional sources (Habr Career, SuperJob)
- [ ] Full Docker + docker-compose setup
- [ ] Webhook deployment

## License

[MIT License](LICENSE)
