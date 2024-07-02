import os 
import yaml
import mlflow
import argparse

TRACKING_URI = 'http://127.0.0.1:5000'


def log_experiment_on_server(experiment_path, exp_name='', is_new_exp=False):
    with open(os.path.join(experiment_path, 'meta.yaml')) as f:
        experiment_meta = yaml.safe_load(f)
    
    experiment_name = experiment_meta['name']


    mlflow.set_tracking_uri(TRACKING_URI)

    # the current experiment is NOT what the user wants to add
    if exp_name != '' and exp_name != experiment_name:
        return ''

    # the current experiment is what the user wants to add to the server OR wants to add all the experiments
    if exp_name != '':
        exp_already_exists = mlflow.get_experiment_by_name(exp_name)
        if is_new_exp and exp_already_exists:
            new_name = input(f"{exp_name} already exists on the server, type a new name or click on Enter to add runs to the existing exp: ")
            if new_name:
                experiment_name = new_name

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

def arg_parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument('--exp_name', type=str, required=False, help="The name of the experiment to add, to the server. If not specified, all the experiments are added", default='')
    parser.add_argument('--new_exp', type=bool, required=False, help="True if it's a new experiment, otherwise False", default=False)
    args = parser.parse_args()
    return args


def main(mlruns_path):
    args = arg_parsing()
    exp_name=''
    is_new_exp=False
    if args.exp_name:
        exp_name = args.exp_name
        is_new_exp = args.new_exp

    added_exp = 0
    for experiment_id in os.listdir(mlruns_path):
        if experiment_id not in ['0', '.trash', 'models']:
            experiment_path = os.path.join(mlruns_path, experiment_id)
            if os.path.isdir(experiment_path):
                server_experiment_id = log_experiment_on_server(experiment_path, exp_name, is_new_exp)
                # if the experiment has been logged (it's either the exp the user wants to add or he wants to add all the experiments)
                if server_experiment_id != '':
                    added_exp += 1
                    for run_id in os.listdir(experiment_path):
                        run_path = os.path.join(experiment_path, run_id)
                        if os.path.isdir(run_path):
                            log_run_on_server(server_experiment_id, run_path)
                    # The only experiment that the user wants to add has been added        
                    if exp_name and server_experiment_id != '':
                        break # We don't finish the iteration


    if added_exp == 0 and args.exp_name:
        print(f"The experiment named '{exp_name}' was not found (locally) - No experiment added to the server")
    else:
        print(f"{added_exp} experiment(s) added to {TRACKING_URI}")


# A régler (il faut ajouter ça comme paramètre du script)
mlruns_path = '/home/getalp/karmouah/Bureau/TutoMLflow/tracking_multiple/tracking_data_2'
if __name__ == '__main__':
    main(mlruns_path)