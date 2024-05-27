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


# Provide an Experiment description that will appear in the UI
experiment_description = (
    "This is the grocery forecasting project. "
    "This experiment contains the produce models for apples."
)


# Provide searchable tags that define characteristics of the Runs that
# will be in this Experiment
experiment_tags = {
    "project_name": "grocery-forecasting",
    "store_dept": "produce",
    "team": "stores-ml",
    "project_quarter": "Q3-2023",
    "mlflow.note.content": experiment_description
}

# Create the Experiment, providing a unique name
produce_apples_experiment = client.create_experiment(
    name="Apple_Models", tags=experiment_tags
)

# Use search_experiments() to search on the project_name tag key
apples_experiment = client.search_experiments(
    filter_string="tags.`project_name`= 'grocery-forecasting'"
)

pprint(vars(apples_experiment[0]))