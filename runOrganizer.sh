# Script for running organizer

source ./envSetup.sh
source ./env/bin/activate

flask run &
cd frontend 
npm start &

function cleanup() {
    kill $(jobs -p)
}

trap cleanup EXIT SIGINT SIGTERM
wait

