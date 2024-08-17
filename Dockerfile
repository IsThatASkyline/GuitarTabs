FROM python:3.10 AS build_app

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app

CMD alembic upgrade head && python -m guitar_app.presentation.tgbot.__main__
