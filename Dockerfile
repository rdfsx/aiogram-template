FROM python:3.9.5-slim-buster

WORKDIR /src
ENV PYTHONPATH "${PYTHONPATH}:/src/"
ENV PATH "/src/scripts:${PATH}"
COPY . /src
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git
RUN python -m pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install
RUN chmod +x /src/scripts/*
ENTRYPOINT ["docker-entrypoint.sh"]
