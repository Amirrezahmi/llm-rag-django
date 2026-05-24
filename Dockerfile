FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY packages/ /packages/
RUN pip install --no-cache-dir --no-index --find-links=/packages -r requirements.txt

COPY tiktoken_cache/ /tmp/data-gym-cache/

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
