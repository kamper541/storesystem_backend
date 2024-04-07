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
EXPOSE 8080

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]