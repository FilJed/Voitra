FROM python:3.11-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    BOT_TOKEN=$BOT_TOKEN \
    OPENAI_API_KEY=$OPENAI_API_KEY

RUN pip install -U pip && \
    pip install poetry

RUN apt-get update && \
    apt-get install -y ffmpeg

WORKDIR /bot

# COPY . .
COPY ./pyproject.toml .

RUN poetry install

COPY . .

CMD [ "python3", "app/bot.py" ]

# ENTRYPOINT [ "/bin/bash" ]