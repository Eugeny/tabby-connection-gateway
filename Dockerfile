FROM python:3.7-alpine AS tabby-connection-gateway

WORKDIR /app
COPY setup.cfg setup.py README.md /app
COPY tabby_connection_gateway tabby_connection_gateway
RUN python setup.py install

ENTRYPOINT ["python", "-m", "tabby_connection_gateway.cli"]
