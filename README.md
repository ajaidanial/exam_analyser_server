# Exam Analyser Server

The backend application for the Exam Analyser app built using Django, Django Rest Framework & Docker.
The application is designed in a detached approach and communicates to the frontend using REST API's.


## Prerequisites
1. Docker & Docker Compose  
2. Python3 & Pip3  
3. Virtualenv  


## Getting Started

### Initial Steps
1. Clone the repository and cd to the project root.  
2. `cp -r .envs.example/ .envs/` and set the necessary values.  

### Development
1. Create a virtual environment in the project root using `virtualenv -p python3 venv`.  
2. Activate the environment.  
3. Install the packages inside `requirements.txt` file.  
4. `docker-compose -f local.yml up`.  
5. Use your text editor, preferably pycharm.  

### Deployment Using Docker
1. Init the staging deployment build `sudo ./scripts/init-docker-staging-nginx-ssl.sh`.  
2. Use `docker-compose` to run all the services `docker-compose -f staging-nginx-ssl.yml up`.  
3. Visit `www.example.com`.  


## Note
1. For more docs, visit the `docs/` folder.  
2. The `./scripts/` folder contains some useful script files.  
3. For running other Django commands use `docker-compose -f <compose_file> run <container_name> <command>`.  
