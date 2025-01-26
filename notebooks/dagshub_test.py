# https://dagshub.com/Apoorv7668/CI-MLOPS.mlflow

import dagshub
dagshub.init(repo_owner='Apoorv7668', repo_name='CI-MLOPS', mlflow=True)

import mlflow
with mlflow.start_run():
  mlflow.log_param('parameter name', 'value')
  mlflow.log_metric('metric name', 1)