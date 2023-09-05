FROM python:3.10 as build_app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app

RUN pip install poetry==1.5.1 && poetry build && pip install ./dist/guitar_app-0.1.0-py3-none-any.whl

CMD alembic upgrade head && python -m guitar_app.presentation.tgbot.__main__
