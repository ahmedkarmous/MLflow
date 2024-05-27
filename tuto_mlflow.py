from mlflow import MlflowClient
from pprint import pprint
from sklearn.ensemble import RandomForestRegressor


# use the tracking server initialzed earlier
client = MlflowClient(tracking_uri="http://127.0.0.1:8080")

# searcing experiments (one exists by default, it encapsulated 
# run information if an explicit Experiment is not declared)
all_experiments = client.search_experiments()

# accessing elements from all_experiments and getting the first one that has the name "Default"
default_experiment = [
    {"name": experiment.name, "lifecycle_stage":experiment.lifecycle_stage}
    for experiment in all_experiments
    if experiment.name == "Default"
][0]

pprint(default_experiment)