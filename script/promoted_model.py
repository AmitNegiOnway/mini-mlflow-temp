import os
import mlflow

def promoted_model():
    # Set up DagsHub credentials for MLflow tracking
    dagshub_token=os.getenv("DAGSHUB_PAT")
    if not dagshub_token:
        raise EnvironmentError("DAGSHUB_PAT environment variable is not set")

    os.environ["MLFLOW_TRACKING_USERNAME"]=dagshub_token
    os.environ["MLFLOW_TRACKING_PASSWORD"]=dagshub_token

    dagshub_url = "https://dagshub.com"
    repo_owner = "amitnegionway"
    repo_name = "mini-mlflow-temp"

    # Set up MLflow tracking URI
    mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')

    client=mlflow.MlflowClient()

    model_name="my_model"

    # get the latest version in staging 

    latest_version_staging=client.get_model_version_by_alias(model_name,alias='staging')[0].version

    # archive the current production model
    champ_version=client.get_model_version_by_alias(model_name,alias='champion')

    if champ_version:
      print(f"Current champion: Version {champ_version.version}")

    # promted the new model to champion 
    client.set_registered_model_alias(
        name=model_name,
        version=latest_version_staging,
        stage="champion"
    )
    print(f"Model version {latest_version_staging} promoted to Production")

if __name__ == "__main__":
    promoted_model()
