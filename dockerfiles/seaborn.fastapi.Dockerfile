FROM registry.devops.svc.k8s.slav.rocks:5000/tb/fastapi

RUN pip install jinja2
RUN pip install seaborn