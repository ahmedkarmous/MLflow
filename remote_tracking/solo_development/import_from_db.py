import mlflow
import psycopg2
from prettytable import PrettyTable
from mlflow_entities import Experiment, Run, Param, Metric, Tag



# URL to connect to the db
DB_URL = "postgresql://user1:password1@localhost:5433/mlflowdb1"

# Id of the experiment we want to add (we can pass it as an argument)
EXPERIMENT_ID = "1"
 
def get_experiment_from_db():
    # Connect to the db
    conn = psycopg2.connect(DB_URL)

    cursor = conn.cursor()


    # Récuperer les données de l'experience
    cursor.execute(f"""
        SELECT name, artifact_location
        FROM experiments
        WHERE experiment_id = {EXPERIMENT_ID}
    """)

    experiment_data = cursor.fetchone()

    if experiment_data is None:
            cursor.close()
            conn.close()
            raise ValueError(f"No experiment found with id {experiment_id}")
        
    name, artifact_location = experiment_data
    experiment = Experiment(name, artifact_location)



    # Récupérer les runs associés à l'expérience
    cursor.execute(f"""
        SELECT run_uuid, name, experiment_id, start_time, end_time, status
        FROM runs
        WHERE experiment_id = {EXPERIMENT_ID}
    """)
    runs_data = cursor.fetchall()
    
    for row in runs_data:
        run_id, name, experiment_id, start_time, end_time, status = row
        run = Run(name, experiment_id,start_time, end_time, status)
        
        # Récupérer les paramètres pour chaque run
        cursor.execute(f"""
            SELECT run_uuid, key, value
            FROM params
            WHERE run_uuid = '{run_id}'
        """)
        params_data = cursor.fetchall()
        for param_row in params_data:
            _, key, value = param_row
            param = Param(key, value)
            run.add_param(param)
        
        # Récupérer les métriques pour chaque run
        cursor.execute(f"""
            SELECT run_uuid, key, value, timestamp, step
            FROM metrics
            WHERE run_uuid = '{run_id}'
        """)
        metrics_data = cursor.fetchall()
        for metric_row in metrics_data:
            _, key, value, timestamp, step = metric_row
            metric = Metric(key, value, timestamp, step)
            run.add_metric(metric)
        
        # Récupérer les tags pour chaque run
        cursor.execute(f"""
            SELECT run_uuid, key, value
            FROM tags
            WHERE run_uuid = '{run_id}'
        """)
        tags_data = cursor.fetchall()
        for tag_row in tags_data:
            _, key, value = tag_row
            tag = Tag(key, value)
            run.add_tag(tag)
        
        experiment.add_run(run)

    # Fermeture du curseur et de la connexion à la base de données
    cursor.close()
    conn.close()
    
    return experiment






SHARED_DB_URL = "postgresql://user:password@localhost:5432/mlflowdb"

def delete_experiment_from_db(experiment_name):
    try:
        # Connexion à la base de données PostgreSQL
        conn = psycopg2.connect(SHARED_DB_URL)
        cursor = conn.cursor()

        # Supprimer les paramètres associés aux runs de l'expérience
        cursor.execute("DELETE FROM params WHERE run_uuid IN (SELECT run_uuid FROM runs WHERE experiment_id = (SELECT experiment_id FROM experiments WHERE name = %s))", (experiment_name,))
        
        # Supprimer les métriques associées aux runs de l'expérience
        cursor.execute("DELETE FROM metrics WHERE run_uuid IN (SELECT run_uuid FROM runs WHERE experiment_id = (SELECT experiment_id FROM experiments WHERE name = %s))", (experiment_name,))
        
        # Supprimer les tags associés aux runs de l'expérience
        cursor.execute("DELETE FROM tags WHERE run_uuid IN (SELECT run_uuid FROM runs WHERE experiment_id = (SELECT experiment_id FROM experiments WHERE name = %s))", (experiment_name,))
        
        # Supprimer les runs de l'expérience
        cursor.execute("DELETE FROM runs WHERE experiment_id = (SELECT experiment_id FROM experiments WHERE name = %s)", (experiment_name,))
        
        # Supprimer l'expérience elle-même
        cursor.execute("DELETE FROM experiments WHERE name = %s", (experiment_name,))
        
        # Valider et appliquer les changements
        conn.commit()
        print(f"Experiment '{experiment_name}' and all associated data have been deleted from the database.")

    except (Exception, psycopg2.Error) as error:
        print(f"Error while deleting experiment '{experiment_name}': {error}")

    finally:
        # Fermer la connexion
        if conn:
            cursor.close()
            conn.close()



if __name__ == '__main__':
    delete_experiment_from_db('experiment1') # add "if exists"
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    experiment = get_experiment_from_db()
    server_experiment_id = mlflow.create_experiment(experiment.name)
    for run in experiment.runs:
        with mlflow.start_run(experiment_id = server_experiment_id, run_name = run.name):
            for param in run.params:
                mlflow.log_param(param.key, param.value)
            for metric in run.metrics:
                mlflow.log_metric(metric.key, metric.value)
            for tag in run.tags:
                mlflow.set_tag(tag.key, tag.value)