FROM python:3.10 as build_app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --upgrade pip && pip install poetry && poetry config virtualenvs.create false


COPY . /app


FROM build_app as prod
ENV PROD 1
RUN poetry install

CMD alembic upgrade head && python -m src.presentation.api.main


