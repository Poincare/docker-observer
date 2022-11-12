export OBSERVER_SETUP_DONE="1"
trap 'x=$?; history 1 >> /root/observer_log.txt; echo "OUTPUT: $x" >> /root/observer_log.txt' DEBUG
