FROM apache/airflow:2.10.4

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER airflow
RUN airflow db init

COPY requirements.txt /tmp/requirements.txt
# RUN pip uninstall bson
RUN pip install --no-cache-dir -r /tmp/requirements.txt