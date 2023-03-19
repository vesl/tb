FROM python:3.9

WORKDIR /code

RUN pip install uvicorn==0.20.0
RUN pip install fastapi==0.91.0
RUN pip install requests==2.28.2
RUN pip install pandas==1.5.3
RUN pip install binance-connector==2.0.0
RUN pip install seaborn==0.12.2
RUN pip install scikit-learn==1.2.1
RUN pip install pymongo==4.3.3
RUN pip install TA-Lib==0.4.25

CMD uvicorn $APP.main:app --host 0.0.0.0 --port 80