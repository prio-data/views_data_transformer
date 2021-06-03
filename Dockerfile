FROM python:3.8

COPY ./requirements.txt /
RUN pip install -r requirements.txt 

COPY ./data_transformer/ /data_transformer/
CMD ["gunicorn","-k","uvicorn.workers.UvicornWorker","--bind","0.0.0.0:80","data_transformer.app:app"]
