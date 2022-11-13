#!/bin/bash

# docker exec -it $(docker ps -q) /bin/bash -c "echo \"PROMPT_COMMAND='history 1 >> /root/observer_commands.txt;'\" >> ~/.bashrc"
# docker exec -it $(docker ps -q) /bin/bash -c "trap 'x=\\\$?; $x >>  /root/observer_outputs.txt' DEBUG"

docker cp ./bashrc_payload.sh $1:/root
docker cp ./add_to_bashrc.sh $1:/root
docker exec -it $1 /bin/bash -c ". /root/add_to_bashrc.sh" 
docker exec -it $1 /bin/bash

docker exec -it $1 /bin/bash -c "cat /root/observer_log.txt" > observer_log.txt
docker exec -it $1 /bin/bash -c "cat /root/observer_checked_in_files.txt" > observer_checked_in_files.txt