import mlflow # global instance instead of MlflowClient,
# it allows for us to use these ‘higher-level’ (simpler) APIs
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from dataset_generator import generate_apple_sales_data_with_promo_adjustment
import numpy as np




mlflow.set_tracking_uri("tracking_data_2")

# Set the current active experiment to the "Apple Models" experiment
# And returns the Experiment metadata
apple_experiment = mlflow.set_experiment("Apple_Models_2")

# Define a run name for this iteration of training.
# If this is not set, a unique name will be auto-generated for the run.
run_name = "apples_rf_test"

# Define an artifact path that the model will be saved to.
artifact_path = "rf_apples"


# Generate a dataset for predicting apple sales demand 
data = generate_apple_sales_data_with_promo_adjustment()

# Split the data into features and target and drop irrelevant date field and target field
X = data.drop(columns=["date", "demand"]) # features
y = data["demand"] # target


# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

params = {
    "n_estimators": 150,  # Augmente le nombre d'arbres dans la forêt
    "max_depth": 8,  # Augmente la profondeur maximale des arbres
    "min_samples_split": 5,  # Réduit le nombre minimal d'échantillons pour diviser un nœud
    "min_samples_leaf": 2,  # Réduit le nombre minimal d'échantillons dans une feuille
    "bootstrap": True,  
    "oob_score": True,  # Active le calcul de l'erreur OOB
    "random_state": 42,  # Change la graine pour assurer la reproductibilité
}


# Train the RandomForestRegressor
rf = RandomForestRegressor(**params)

# Fit the model on the training data (ça fait partie aussi de l'entraînement)
rf.fit(X_train, y_train)

# Predict on the validation set
y_pred = rf.predict(X_val)

# Calculate error metrics
mae = mean_absolute_error(y_val, y_pred)
mse = mean_squared_error(y_val, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_val, y_pred)


# Assemble the metrics we're going to write into a collection
metrics = {"mae": mae, "mse": mse, "rmse": rmse, "r2": r2}


# Initiate the Mlflow run context
with mlflow.start_run(run_name=run_name) as run: 
    # Log the parameters used for the model fit
    mlflow.log_params(params)

    # Log the error metrics that were calculated during validation
    mlflow.log_metrics(metrics)

    # Log an instance of the trained model for later use
    mlflow.sklearn.log_model(
        sk_model=rf, input_example=X_val, artifact_path=artifact_path
    )