FROM python:3.13-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* /app/

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . /app/

CMD ["poetry", "run", "python", "generator.py"]