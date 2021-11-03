FROM prioreg.azurecr.io/prio-data/uvicorn_deployment:1.3.0
COPY ./requirements.txt /
RUN pip install -r requirements.txt 
COPY ./data_transformer/ /data_transformer/
ENV APP data_transformer.app:app
