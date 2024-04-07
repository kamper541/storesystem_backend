FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV APP_HOME /app
ENV TZ 'Asia/Bangkok'


WORKDIR $APP_HOME

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD exec gunicorn --bind 0.0.0.0:8000 --workers 4 --threads 6 --timeout 0 --worker-class uvicorn.workers.UvicornWorker sstm.wsgi:application