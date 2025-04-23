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


SELECT *
FROM transactions_v2;

-- 4.1
SELECT currency, sum(amount) AS total_amount
FROM transactions_v2
WHERE currency IN ('USD', 'EUR', 'RUB')
GROUP BY currency;

/*
currency|total_amount|
--------+------------+
EUR     |        2172|
RUB     |         320|
USD     |       12264|*/

-- 4.2
SELECT transaction_type,
       SUM(amount) AS total_amount,
       ROUND(AVG(amount),2) AS avg_amount
FROM (
SELECT CASE WHEN is_fraud = 1 THEN 'fraud' ELSE 'legit' END AS transaction_type,
       *
FROM transactions_v2 AS t
) AS t2
GROUP BY transaction_type


/*
transaction_type|total_amount|avg_amount|
----------------+------------+----------+
fraud           |       12171|   1217.10|
legit           |        3654|    365.40|*/


-- 4.3
SELECT CAST(transaction_date AS DATE) AS transaction_date,
       COUNT(transaction_id) AS transactions_cnt,
       SUM(amount) AS total_amount,
       ROUND(AVG(amount),2) AS avg_amount
FROM transactions_v2 tv
GROUP BY CAST(transaction_date AS DATE)
ORDER BY CAST(transaction_date AS DATE)


/*
transaction_date|transactions_cnt|total_amount|avg_amount|
----------------+----------------+------------+----------+
      2023-03-10|               4|         941|    235.25|
      2023-03-11|               4|        1870|    467.50|
      2023-03-12|               4|         896|    224.00|
      2023-03-13|               4|       10744|   2686.00|
      2023-03-14|               4|        1374|    343.50|
 **/

-- 4.4

SELECT CAST(transaction_date AS DATE) AS transaction_date,
       COUNT(transaction_id) AS transactions_cnt,
       SUM(amount) AS total_amount,
       ROUND(AVG(amount),2) AS avg_amount
FROM transactions_v2 tv
WHERE day(transaction_date) BETWEEN 11 AND 12
GROUP BY CAST(transaction_date AS DATE)
ORDER BY CAST(transaction_date AS DATE)

/*
transaction_date|transactions_cnt|total_amount|avg_amount|
----------------+----------------+------------+----------+
      2023-03-11|               4|        1870|    467.50|
      2023-03-12|               4|         896|    224.00|
*/


-- 4.5

SELECT t.transaction_id, category, count(log_id) AS logs_cnt
FROM transactions_v2 t
INNER JOIN logs_V2 l ON l.transaction_id = t.transaction_id
GROUP BY t.transaction_id, category
ORDER BY count(log_id) DESC

/*
transaction_id|category   |logs_cnt|
--------------+-----------+--------+
         10010|Electronics|       2|
         10001|Electronics|       1|
         10002|Travel     |       1|
         10004|System     |       1|
         10006|Electronics|       1|
         10007|Misc       |       1|
         10013|Misc       |       1|
         10014|Electronics|       1|
         10015|Other      |       1|
         10019|Travel     |       1|
         10020|Misc       |       1|
 */
