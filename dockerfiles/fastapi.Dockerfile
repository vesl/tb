FROM python:3.9

WORKDIR /code

RUN pip install uvicorn fastapi
RUN pip install requests

CMD uvicorn $APP.main:app --host 0.0.0.0 --port 80
