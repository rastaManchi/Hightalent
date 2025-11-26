FROM python:3.10


WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .


CMD python manage.py collectstatic --no-input && \
    python manage.py migrate --no-input && \
    python manage.py runserver