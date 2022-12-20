FROM registry.devops.svc.k8s.slav.rocks:5000/tb/talib.fastapi

RUN pip install scikit-learn
RUN pip install pymongo
