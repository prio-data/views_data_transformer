FROM views3/uvicorn-deployment:2.1.0

COPY ./requirements.txt /
RUN pip install -r requirements.txt 

COPY ./data_transformer/ /data_transformer/

ENV GUNICORN_APP data_transformer.app:app
