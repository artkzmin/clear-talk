# ClearTalk

ClearTalk — это чат-бот, выступающий в роли ИИ-психолога. Пользователь пересылает боту переписку или голосовые сообщения, и система анализирует их с точки зрения эмоционального фона, характера общения и психологических паттернов. На основе анализа бот даёт советы по межличностным отношениям.

## 📌 Основные функции

- 📃 Анализ текстовых переписок
- 🎙 Распознавание и анализ голосовых сообщений (с помощью Whisper от OpenAI)
- 💬 Генерация советов по улучшению межличностных отношений
- 🌐 Поддержка русского языка

## 🚀 Технологии

- Python 3.11
- OpenAI Whisper (ASR + TTS)
- OpenAI GPT
- FastAPI
- Aiogram
- PostgreSQL
- Pydantic v2
- SQLAlchemy v3
- Alembic
- Docker / Docker Compose
- GitLab CI

## ⚙ Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/artkzmin/clear-talk.git
   cd clear-talk
   ```

2. Создайте файл `.env` в директории `config` на основе `.env.dist`:
   ```bash
   cp config/.env.dist config/.env
   ```

3. Запустите сборку и запуск проекта с помощью Makefile:
   ```bash
   make docker-run
   ```
