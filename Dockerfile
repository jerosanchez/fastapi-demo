FROM python:3.13-trixie AS base
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS migrate
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini .
CMD [ "alembic", "upgrade", "head" ]

FROM base AS development
COPY .env .
COPY app/ ./app/
CMD [ "fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000" ]

FROM base AS production
COPY app/ ./app/
CMD [ "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000" ]