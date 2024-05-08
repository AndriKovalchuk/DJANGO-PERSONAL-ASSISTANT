ARG PYTHON_VERSION=3.12-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV APP_HOME /app

WORKDIR $APP_HOME

# install psycopg2 dependencies.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY poetry.lock pyproject.toml $APP_HOME/

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install

COPY Personal_Assistant_WEB/ .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]