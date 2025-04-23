 CREATE EXTERNAL TABLE IF NOT EXISTS transactions_v2 (
    transaction_id BIGINT,
    user_id BIGINT,
    amount NUMERIC,
    currency varchar(5),
    transaction_date TIMESTAMP,
    is_fraud boolean
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION 's3a://storage.yandexcloud.net/winterbaket/transactions_v2.csv';



CREATE EXTERNAL  TABLE  IF NOT EXISTS logs_v2 (
    log_id BIGINT,
    transaction_id BIGINT,
    category varchar(50),
    comment varchar(250),
    log_timestamp TIMESTAMP
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION 's3a://storage.yandexcloud.net/winterbaket/logs_v2.txt';