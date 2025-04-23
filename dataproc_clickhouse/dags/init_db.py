import os
import sqlite3
import logging

import requests
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.task_group import TaskGroup

# from utils.db_conn import get_clickhouse_connection

logger = logging.getLogger(__name__)
dag_name = os.path.splitext(os.path.basename(__file__))[0]
cur_dir = os.path.abspath(os.path.dirname(__file__))

clickhouse_user, clickhouse_pass = 'admin', '****'

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

hive_queries = (
    """
    SELECT *
    
    """
)


def get_data_clickhouse(query, logger) -> None:
    response = requests.get(
        'https://{0}:8443'.format('rc1d-rb45b5o0avh16ld2.mdb.yandexcloud.net'),
        params={
            'query': query,
        },
        headers={
            'X-ClickHouse-User': clickhouse_user,
            'X-ClickHouse-Key': clickhouse_pass,
        },
        verify='/usr/local/share/ca-certificates/Yandex/RootCA.crt'
    )
    logger.info(response.text)
    return response.text




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