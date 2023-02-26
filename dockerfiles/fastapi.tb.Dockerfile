FROM python:3.9

WORKDIR /code

RUN pip install uvicorn fastapi
RUN pip install requests
RUN pip install pandas
RUN pip install binance-connector
RUN pip install seaborn
RUN pip install scikit-learn
RUN pip install pymongo
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz -O /tmp/ta-lib-0.4.0-src.tar.gz
RUN cd /tmp/ && tar -xzvf ta-lib-0.4.0-src.tar.gz
RUN cd /tmp/ta-lib/ && ./configure --prefix=/usr && make && make install
RUN pip install TA-Lib

CMD uvicorn $APP.main:app --host 0.0.0.0 --port 80