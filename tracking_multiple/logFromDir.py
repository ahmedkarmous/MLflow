import os 
import yaml
import mlflow
import argparse

TRACKING_URI = 'http://127.0.0.1:5000'


def log_experiment_on_server(experiment_path, exp_name='', is_new_exp="False"):
    # if the experiment has no runs, we do nothing, there's no reason to create an experiment
    runs = os.listdir(experiment_path) # os.listdir affiche liste les dossiers et les fichiers, d'où la ligne 30
    # check if the experiment folder contains any run folders
    if runs == ['meta.yaml']: 
        print(f"No runs associated with the experiment {exp_name}. Experiment NOT added.")
        return ''
    
    mlflow.set_tracking_uri(TRACKING_URI)
    # check if the experiment already exists on the server (using the name)
    exp_already_exists = mlflow.get_experiment_by_name(exp_name)
    # if the experiment already exists and the user specified that it's a new experiment, we ask him if he wants to change the name or log runs to the existing experiment
    if is_new_exp in ["True", "true", "T", "t"] and exp_already_exists:
        new_name = input(f"{exp_name} already exists on the server, type a new name or click on Enter to add runs to the existing exp: ")
        if new_name:
            exp_name = new_name
    
    server_experiment = mlflow.set_experiment(experiment_name=exp_name)
    for run_id in os.listdir(experiment_path):
        run_path = os.path.join(experiment_path, run_id)
        if os.path.isdir(run_path):
            log_run_on_server(server_experiment.experiment_id, run_path)
    return server_experiment.experiment_id


def log_run_on_server(experiment_id, run_path):
    with open(os.path.join(run_path, 'meta.yaml')) as f:
        run_meta = yaml.safe_load(f)

    run_name = run_meta['run_name']
    
    # If necessary, treat the name conflict of runs (multiple runs have the same name)
    
    with mlflow.start_run(experiment_id=experiment_id, run_name=run_name) as run:
        # log params
        params_path = os.path.join(run_path, 'params')
        if os.path.exists(params_path):
            for param in os.listdir(params_path):
                with open(os.path.join(params_path, param)) as f:
                    value = f.read()
                    ############### mlflow ###############
                    mlflow.log_param(param, value)
                    ############### mlflow ###############

        # log metrics
        metrics_path = os.path.join(run_path, 'metrics')
        if os.path.exists(metrics_path):
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
    parser.add_argument('--tracking_data_path', type=str, required=True, help="The path to the tracking data generated by mlflow")
    parser.add_argument('--exp_name', type=str, required=False, help="The name of the experiment to add, to the server. If not specified, all the experiments are added", default='')
    parser.add_argument('--new_exp', type=str, required=False, help="True if it's a new experiment, otherwise False", default=False, choices=["True", "true", "T", "t", "False", "false", "F", "f"])
    args = parser.parse_args()
    return args


def main():
    args = arg_parsing()
    mlruns_path = args.tracking_data_path
    exp_name=''
    is_new_exp="False"
    if args.exp_name:
        exp_name = args.exp_name
        is_new_exp = args.new_exp

    exp_added = 0
    exp_found = 0
    server_experiment_id = ''
    for experiment_id in os.listdir(mlruns_path):
        if experiment_id not in ['0', '.trash', 'models']:
            experiment_path = os.path.join(mlruns_path, experiment_id)
            if os.path.isdir(experiment_path):
                # check if the experiment name is equal to the experiment name the user wants to add
                with open(os.path.join(experiment_path, 'meta.yaml')) as f:
                    experiment_meta = yaml.safe_load(f)
                    experiment_name = experiment_meta['name']
                    # we log the experiment only if it's name is as specified or the user didn't specify a name and wants to log all the experiments
                    if (exp_name == '') or (exp_name != '' and experiment_name == exp_name):
                        exp_found += 1
                        server_experiment_id = log_experiment_on_server(experiment_path, exp_name, is_new_exp)
                # if the experiment has been logged (it's either the exp the user wants to add or he wants to add all the experiments)
                if server_experiment_id != '':
                    exp_added += 1
                    # The only experiment that the user wants to add has been added        
                    if exp_name and server_experiment_id != '':
                        break # We don't finish the iteration


    if exp_found == 0 and args.exp_name:
        print(f"The experiment named '{exp_name}' was not found (locally) - No experiment added to the server")
    elif exp_added > 0:
        print(f"{exp_added} experiment(s) added to {TRACKING_URI}")


# mlruns_path = '/home/getalp/karmouah/Bureau/TutoMLflow/tracking_multiple/tracking_data_2'
if __name__ == '__main__':
    main()