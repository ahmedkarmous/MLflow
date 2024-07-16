import mlflow
import psycopg2

from sklearn.model_selection import train_test_split
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor

SOLO_DB_URL = "postgresql://user1:password1@localhost:5433/mlflowdb1"
SHARED_DB_URL = "postgresql://user:password@localhost:5432/mlflowdb"


def delete_all_experiments_from_db(DB_URL):
    try:
        # Connexion à la base de données PostgreSQL
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()

        # Supprimer les paramètres
        cursor.execute("DELETE FROM params")
        
        # Supprimer les métriques
        cursor.execute("DELETE FROM metrics")
        
        # Supprimer les tags
        cursor.execute("DELETE FROM tags")

        cursor.execute("DELETE FROM latest_metrics")
        
        # Supprimer les runs
        cursor.execute("DELETE FROM runs")

        cursor.execute("DELETE FROM datasets")
        
        # Supprimer les expériences
        cursor.execute("DELETE FROM experiments")
        
        # Valider et appliquer les changements
        conn.commit()
        print("All experiments and associated data have been deleted from the database.")

    except (Exception, psycopg2.Error) as error:
        print(f"Error while deleting all experiments: {error}")

    finally:
        # Fermer la connexion
        if conn:
            cursor.close()
            conn.close()



# On vide la base à chaque fois pour ne pas ajouter des exp déjà existantes sur le serveur commun
delete_all_experiments_from_db(SOLO_DB_URL)

# delete_all_experiments_from_db(SHARED_DB_URL)


mlflow.set_tracking_uri("postgresql://user1:password1@localhost:5433/mlflowdb1")

mlflow.set_experiment("experiment_test_2")

mlflow.sklearn.autolog()

db = load_diabetes()
X_train, X_test, y_train, y_test = train_test_split(db.data, db.target)

# Create and train models.
rf = RandomForestRegressor(n_estimators=100, max_depth=6, max_features=3)
rf.fit(X_train, y_train)

# Use the model to make predictions on the test dataset.
predictions = rf.predict(X_test)