FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV APP_HOME /app
ENV TZ 'Asia/Bangkok'
ENV PORT 8000

WORKDIR $APP_HOME

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 6 --timeout 0 --worker-class uvicorn.workers.UvicornWorker cpp.asgi:application