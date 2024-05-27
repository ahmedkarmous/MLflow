from mlflow import MlflowClient
from pprint import pprint
from sklearn.ensemble import RandomForestRegressor


# use the tracking server initialzed earlier
client = MlflowClient(tracking_uri="http://127.0.0.1:8080")

# searcing experiments (one exists by default, it encapsulated 
# run information if an explicit Experiment is not declared)

