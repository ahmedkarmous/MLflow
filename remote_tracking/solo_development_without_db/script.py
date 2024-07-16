import mlflow

from sklearn.model_selection import train_test_split
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor

# on peut préciser un chemin pour stocker les données de tracking, par défaut, c'est dans mlruns/
# il faut vider le dossier de tracking avant chaque import

mlflow.set_experiment("experiment_test_6")

mlflow.sklearn.autolog()

db = load_diabetes()
X_train, X_test, y_train, y_test = train_test_split(db.data, db.target)

# Create and train models.
rf = RandomForestRegressor(n_estimators=100, max_depth=6, max_features=3)
rf.fit(X_train, y_train)

# Use the model to make predictions on the test dataset.
predictions = rf.predict(X_test)