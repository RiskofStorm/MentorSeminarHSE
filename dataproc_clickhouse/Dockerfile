FROM apache/airflow:2.10.4

USER root
RUN apt-get update && apt-get install wget -y
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN  mkdir --parents /usr/local/share/ca-certificates/Yandex && \
sudo wget "https://storage.yandexcloud.net/cloud-certs/RootCA.pem" \
   --output-document /usr/local/share/ca-certificates/Yandex/RootCA.crt && \
sudo wget "https://storage.yandexcloud.net/cloud-certs/IntermediateCA.pem" \
   --output-document /usr/local/share/ca-certificates/Yandex/IntermediateCA.crt && \
sudo chmod 655 \
   /usr/local/share/ca-certificates/Yandex/RootCA.crt \
   /usr/local/share/ca-certificates/Yandex/IntermediateCA.crt && \
sudo update-ca-certificates

USER airflow
RUN airflow db init


COPY hse_dataproc /tmp/hse_dataproc
COPY requirements.txt /tmp/requirements.txt
# RUN pip uninstall bson
RUN pip install --no-cache-dir -r /tmp/requirements.txt