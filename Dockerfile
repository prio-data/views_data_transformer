FROM prioreg.azurecr.io/prio-data/uvicorn_deployment:2.0.0
USER gunicorn

COPY ./requirements.txt /
RUN pip install -r requirements.txt 

COPY ./data_transformer/ /data_transformer/

ENV GUNICORN_APP data_transformer.app:app
