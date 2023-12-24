FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

ENV PIP_ROOT_USER_ACTION=ignore

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic --noinput

COPY mysite .

CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]