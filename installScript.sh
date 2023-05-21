# Script for setting up the organizer installation

source envSetup.sh

# make the database:
python3.9 database/initializeDB


# install backend dependencies
python3.9 -m virtualenv env
source env/bin/activate
pip install -r requirements.txt


# install frontend dependencies
cd frontend
npm install package.json

