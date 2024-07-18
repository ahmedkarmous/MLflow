# /!\ CHECK the repo: remote_tracking/ (For importing tracking data)


# Introduction : 
This repository contains the code to set up three tracking instances:
1. A common team tracking server (remote): This is the server that aggregates the experiments shared by the team.
2.A tracking server without a database: Experiments are stored locally in a folder.
3. A tracking server with a database: Experiments are stored in a database (in this case, a PostgreSQL database).

## 1- Launching the common tracking server: (remote_tracking/)
- Instead of using multiple remote hosts as in production, a single machine with multiple Docker containers will be used. MinIO, an S3-compatible storage, will serve as the artifact store, eliminating the need for an AWS account.

Using Docker Compose, we will have two environments:
+ PostgreSQL database: backend store.
+ MinIO server: artifact store.

To launch the containers:
```bash
docker compose up -d
```

Configure the access for the S3 server:
```bash
export MLFLOW_S3_ENDPOINT_URL=http://localhost:9000 # Replace this with remote storage endpoint e.g. s3://my-bucket in real use cases
export AWS_ACCESS_KEY_ID=minio_user
export AWS_SECRET_ACCESS_KEY=minio_password

```

Launch the tracking server
```bash
mlflow server \
  --backend-store-uri postgresql://user:password@localhost:5432/mlflowdb \
  --artifacts-destination s3://bucket \
  --host 0.0.0.0 \
  --port 5000
```

- Run a tracking script (that generates tracking data stored in the database) after setting the tracking url to [ http://127.0.0.1:5000 ](http://127.0.0.1:5000) (replace with remote host name or IP address in actual environment)
This can be done by executing this line in the terminal:
```bash
export MLFLOW_TRACKING_URI=http://127.0.0.1:5000  # or host name or IP address in an actual environment
```
or by adding to the script this line:
```python
mlflow.set_tracking_uri("http://127.0.0.1:5000 ") 
```

Note: **pyscopg2** and **boto3** are required for accessing PostgreSQL and S3 with Python

- You can access the UI by navigating to [ http://127.0.0.1:5000 ](http://127.0.0.1:5000) (replace with remote host name or IP address in actual environment) in your browser.



## 2- Launching the tracking server without a database: (solo_development_without_db/)
- You can delete the folder **mlruns/** in order to start from scratch and create a new set of experiments 
- To do so, run **script.py** (an example of an mlflow tracking script) after setting the name of the experiment to create
- Once this is done, the experiment(s) created are added in the **mlruns/** folder from which you need to import the tracking data to the remote tracking server (the server of the team)
- To import the tracking data, run the script **import_from_dir.py**:
```bash
python import_from_dir.py --tracking_data_path "mlruns/" \ --tracking_server_url "http://127.0.0.1:5000"
```
- After doing these steps, you should be able to see the experiment(s) you created logged on the tracking server [ http://127.0.0.1:5000 ](http://127.0.0.1:5000)




## 3- Launching the tracking server with a database: (solo_development_with_db/)
- In a new terminal, launch the docker container to set a postgres database in which you're gonna store the tracking data:
```bash
docker compose up -d
```
- To create experiments and store them in the databse (the artifacts are stored locally in the folder **mlruns/**), run the script **script.py** after setting the name of the experiment(s):
Note: **script.py** contains a function to delete all the experiments from a database called *delete_all_experiments_from_db* . This function can be primarily used for testing, to empty either the team database or the developer's personal database (in case he wants to add a new set of experiments to the shared server)
- In order to add the experiments that you just created, you need to run the script **import_from_db.py**:
```bash
python import_from_db.py --db_url \
"postgresql://user1:password1@localhost:5433/ mlflowdb1" \
--tracking_url "http://127.0.0.1:5000"
```
- Once these steps are done, you should be able to see all the experiments stored in your personal database logged on the tracking server [ http://127.0.0.1:5000 ](http://127.0.0.1:5000)