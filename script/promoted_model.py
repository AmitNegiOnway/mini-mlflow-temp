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

    latest_version_staging=client.get_latest_versions(model_name,stages=['champion'])[0].version

    # archive the current production model
    prod_version=client.get_latest_versions(model_name,stages=['champion'])

    for version in prod_version:
        client.transition_model_version_stage(
            name=model_name,
            version=version.version,
            stage='Archived'
        )
    # promted the new model to production 
    client.transition_model_version_stage(
        name=model_name,
        version=latest_version_staging,
        stage="Production"
    )
    print(f"Model version {latest_version_staging} promoted to Production")

if __name__ == "__main__":
    promoted_model()
