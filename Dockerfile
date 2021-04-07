FROM python:3.8

COPY ./requirements.txt /
RUN pip install -r requirements.txt 

COPY ./transform/ /transform/
CMD ["gunicorn","-k","uvicorn.workers.UvicornWorker","--bind","0.0.0.0:80","transform.app:app"]
