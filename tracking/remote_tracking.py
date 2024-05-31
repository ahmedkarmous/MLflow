import mlflow

from sklearn.model_selection import train_test_split
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor


mlflow.set_tracking_uri("http://127.0.0.1:5000")

# réduit le besoin d'ajouter manuellement du code pour enregistrer les paramètres, les métriques, les artefacts, et les modèles.
mlflow.autolog()

db = load_diabetes()
X_train, X_test, y_train, y_test = train_test_split(db.data, db.target)

# Create and train models
rf = rf = RandomForestRegressor(n_estimators=100, max_depth=6, max_features=3)
rf.fit(X_train, y_train)

# Use the model to make predicitons on the test dataset
predictions = rf.predict(X_test)


run_id = "5bc2d9920fff4e3a91ea3d01d260502e"
artifact_path = "model"

# Download the artifact via the tracking server
mlflow_artifact_uri = f"runs:/{run_id}/{artifact_path}"
local_path = mlflow.artifacts.download_artifacts(mlflow_artifact_uri)

# Load the model
model = mlflow.sklearn.load_model(local_path)