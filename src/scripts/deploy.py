import os
import subprocess

def deploy_model(model_path, deployment_path):
    """
    Deploy the machine learning model to the specified deployment path.
    
    Args:
        model_path (str): The path to the trained model.
        deployment_path (str): The path where the model should be deployed.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")

    # Copy the model to the deployment path
    subprocess.run(["cp", model_path, deployment_path], check=True)
    print(f"Model deployed to {deployment_path}")

if __name__ == "__main__":
    # Example usage
    model_path = "path/to/trained/model"  # Update with the actual model path
    deployment_path = "path/to/deployment"  # Update with the actual deployment path
    deploy_model(model_path, deployment_path)