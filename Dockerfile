FROM prioreg.azurecr.io/uvicorn-deployment 
COPY ./requirements.txt /
RUN pip install -r requirements.txt 
COPY ./data_transformer/ /data_transformer/
ENV APP="data_transformer.app:app"
