FROM registry.devops.svc.k8s.slav.rocks:5000/tb/fastapi

RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz -O /tmp/ta-lib-0.4.0-src.tar.gz
RUN cd /tmp/ && tar -xzvf ta-lib-0.4.0-src.tar.gz
RUN cd /tmp/ta-lib/ && ./configure --prefix=/usr && make && make install

RUN pip install TA-Lib
