# GTSAM-OPT-Server

### Installing dependencies

I highly recommend using conda or at least virtualenv to manage your environment.
In any case, cd in `flask_server` and type `pip install -r requirements.txt` to install
backend modules. In `frontend`, type `npm install` to install any node components.

### How to run

This project has two components: a Flask server and a React frontend. 
As a design decision, these two services are decoupled from one another,
so you'll need to run them separately.

To run the server, cd into the `flask_server` folder. Type `export FLASK_APP=run.py`
Type flask run.

To run the frontend, cd into `frontend` and type `npm start`.
