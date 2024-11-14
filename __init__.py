#__init__.py
import logging
import git
import os
import subprocess
import azure.functions as func

# Path to the folder where you want to clone the repository
#cambio trascendental
repo_folder = "/tmp/myrepo"

# Git repo URL
repo_url = "https://github.com/your-username/myrepo.git"

def main(mytimer: func.TimerRequest) -> None:
    # Log the event
    logging.info('Python timer trigger function started')

    # Check if the repo folder exists
    if not os.path.exists(repo_folder):
        os.makedirs(repo_folder)

    # Clone the repo if it does not exist
    if not os.path.exists(os.path.join(repo_folder, ".git")):
        logging.info("Cloning the repository")
        git.Repo.clone_from(repo_url, repo_folder)
    else:
        # Pull the latest changes if the repo exists
        logging.info("Pulling latest changes from the repo")
        repo = git.Repo(repo_folder)
        origin = repo.remotes.origin
        origin.pull()

    # Now execute the Python script 'main.py'
    script_path = os.path.join(repo_folder, 'main.py')
    if os.path.exists(script_path):
        try:
            # Execute main.py using subprocess
            subprocess.run(["python", script_path], check=True)
            logging.info("Executed main.py successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing main.py: {e}")
    else:
        logging.error("main.py not found in the repository.")