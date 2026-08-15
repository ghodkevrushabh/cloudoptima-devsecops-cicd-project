FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN groupadd --gid 1000 cloudoptima \
    && useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash cloudoptima

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend

RUN mkdir -p /app/generated \
    && chown -R cloudoptima:cloudoptima /app

WORKDIR /app/backend

USER cloudoptima

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
