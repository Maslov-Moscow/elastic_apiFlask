FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./app /app

RUN pip install --no-deps -r requirements.txt