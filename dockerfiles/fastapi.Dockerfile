FROM python:3.9

WORKDIR /code

RUN pip install uvicorn fastapi

CMD ["uvicorn", "app.main:$APP", "--host", "0.0.0.0", "--port", "80"]