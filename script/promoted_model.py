import os
import mlflow

def promoted_model():
    # Set up DagsHub credentials
    dagshub_token = os.getenv("DAGSHUB_PAT")
    if not dagshub_token:
        raise EnvironmentError("DAGSHUB_PAT environment variable is not set")

    os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

    dagshub_url = "https://dagshub.com"
    repo_owner = "amitnegionway"
    repo_name = "mini-mlflow-temp"

    mlflow.set_tracking_uri(
        f"{dagshub_url}/{repo_owner}/{repo_name}.mlflow"
    )

    client = mlflow.MlflowClient()

    model_name = "my_model"

    # Get staging model
    latest_version_staging = client.get_model_version_by_alias(
        model_name,
        alias="staging"
    ).version

    # Get current champion (optional)
    try:
        champ_version = client.get_model_version_by_alias(
            model_name,
            alias="champion"
        )
        print(f"Current champion: Version {champ_version.version}")
    except Exception:
        print("No champion model found.")

    # Promote staging -> champion
    client.set_registered_model_alias(
        name=model_name,
        alias="champion",
        version=latest_version_staging
    )

    print(f"Model version {latest_version_staging} promoted to champion")

if __name__ == "__main__":
    promoted_model()