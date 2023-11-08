# Script for running organizer

source ~/Documents/tools/organizer/envSetup.sh
source ~/Documents/tools/organizer/env/bin/activate

cd ~/Documents/tools/organizer
flask run &
cd frontend 
npm start &

function cleanup() {
    kill $(jobs -p)
}

trap cleanup EXIT SIGINT SIGTERM
wait

