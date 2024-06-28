import os 
import yaml
import mlflow



def log_experiment_on_server(experiment_path):
    with open(os.path.join(experiment_path, 'meta.yaml')) as f:
        experiment_meta = yaml.safe_load(f)
    
    experiment_name = experiment_meta['name'] + '2.0'


    mlflow.set_tracking_uri('http://127.0.0.1:8080')
    server_experiment = mlflow.set_experiment(experiment_name=experiment_name)
    return server_experiment.experiment_id


def log_run_on_server(experiment_id, run_path):
    with open(os.path.join(run_path, 'meta.yaml')) as f:
        run_meta = yaml.safe_load(f)

    with mlflow.start_run(experiment_id=experiment_id, run_name=run_meta['run_name']) as run:
        # log params
        params_path = os.path.join(run_path, 'params')
        for param in os.listdir(params_path):
            with open(os.path.join(params_path, param)) as f:
                value = f.read()
                ############### mlflow ###############
                mlflow.log_param(param, value)
                ############### mlflow ###############

        # log metrics
        metrics_path = os.path.join(run_path, 'metrics')
        for metric in os.listdir(metrics_path):
            with open(os.path.join(metrics_path, metric)) as f:
                first_line = f.readline()
                values = first_line.split()
                value = float(values[1])
                ############### mlflow ###############
                mlflow.log_metric(metric, value)
                ############### mlflow ###############

        # log tags
        tags_path = os.path.join(run_path, 'tags')
        if os.path.exists(tags_path):
            for tag in os.listdir(tags_path):
                with open(os.path.join(tags_path, tag)) as f:
                    value = f.read()
                mlflow.set_tag(tag, value)




def main(mlruns_path):
    for experiment_id in os.listdir(mlruns_path):
        if not experiment_id in ['0', '.trash', 'models']:
            experiment_path = os.path.join(mlruns_path, experiment_id)
            if os.path.isdir(experiment_path):
                server_experiment_id = log_experiment_on_server(experiment_path)
                for run_id in os.listdir(experiment_path):
                    run_path = os.path.join(experiment_path, run_id)
                    if os.path.isdir(run_path):
                        log_run_on_server(server_experiment_id, run_path)


mlruns_path = 'mlruns/'
if __name__ == '__main__':
    main(mlruns_path)