import datetime as dt
import os
import sys

from airflow.models import DAG
from airflow.operators.python import PythonOperator

path = '/opt/airflow'
# Добавим путь к коду проекта в переменную окружения, чтобы он был доступен python-процессу
os.environ['PROJECT_PATH'] = path
# Добавим путь к коду проекта в $PATH, чтобы импортировать функции
sys.path.insert(0, path)

from modules.pipeline import pipeline
from modules.predict import predictt

args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2024, 12, 15),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
    'depends_on_past': True,
    'catchup': False
}

with DAG(
        dag_id='car_price_prediction',
        schedule="00 15 * * *",
        default_args=args,
) as dag:
    task_pipeline = PythonOperator(
        task_id='Pipeline',
        python_callable=pipeline,
        dag=dag
    )
    task_predict = PythonOperator(
        task_id='Predict',
        python_callable=predictt,
        dag=dag
    )

    task_pipeline >> task_predict
