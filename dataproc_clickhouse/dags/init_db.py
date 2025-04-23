import os
import sqlite3
import logging

import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.task_group import TaskGroup

from utils.db_conn import get_clickhouse_connection

logger = logging.getLogger(__name__)
dag_name = os.path.splitext(os.path.basename(__file__))[0]
cur_dir = os.path.abspath(os.path.dirname(__file__))

default_args = {
    'owner': 'Airflow',
    'start_date': pendulum.datetime(2025, 4, 1),
    'retries': 0,
    'schedule': None,
    'email_on_retry': False,
    'depends_on_past': False,
    'email': None,
    'email_on_failure': False
}

dag = DAG(
    dag_id=dag_name,
    default_args=default_args,
    max_active_runs=1,
    description=f'initializing task for db instances',
    schedule_interval=None,
    catchup=False,
    tags=['HSE', 'INITDB', ],
)

start_dag = DummyOperator(
    dag=dag,
    task_id='start_dag',
)

end_dag = DummyOperator(
    dag=dag,
    task_id='end_dag',
)

tg_init_db = TaskGroup(
    group_id='init_db_tasks',
    dag=dag,
)

clickhouse_ddls = [
    "CREATE SCHEMA IF NOT EXISTS stg;",
    """
    CREATE TABLE IF NOT EXISTS stg.transactions_v2 (
        transaction_id Int32,
        user_id Int32,
        amount float,
        currency string,
        transaction_date DateTime('Europe/Moscow'),
        is_fraud Bool
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS stg.logs_v2 (
        log_id Int32,
        transaction_id Int32,
        category string,
        comment string,
        log_timestamp DateTime('Europe/Moscow')
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS stg.orders
        order_id Int32,
        user_id Int32,
        order_date DateTime('Europe/Moscow'),
        total_amount float,
        payment_status string
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS stg.order_items(
        item_id Int32,
        order_id Int32,
        product_name string,
        product_price float,
        quantity Int32
    )
    """,
    """
    INSERT INTO stg.orders
       SELECT *
       FROM s3('https://storage.yandexcloud.net/winterbaket/orders.csv', 'csv');
    """,
    """
    INSERT INTO stg.order_items
    SELECT *
    FROM s3('https://storage.yandexcloud.net/winterbaket/order_items.txt', 'csv');
    """
]


def init_clickhouse(clickhouse_ddls, logger) -> None:
    conn = get_clickhouse_connection()
    cur = conn.cursor()
    for query in clickhouse_ddls:
        logger.info(f'EXECUTING SQL QUERY {query}')
        cur.execute(query)

    conn.commit()
    conn.close()
    logger.info(f"CREATED CLICKHOUSE TABLES ")





click_init = PythonOperator(
    dag=dag,
    task_id='sqlite3_init',
    task_group=tg_init_db,
    python_callable=init_clickhouse,
    op_kwargs={
        'clickhouse_ddls': clickhouse_ddls,
        'logger': logger,
    },
)



start_dag >> tg_init_db >> end_dag