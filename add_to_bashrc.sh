source ~/.bashrc

if [ "$OBSERVER_SETUP_DONE" = "1" ]; then
	echo "nothing to be done with bashrc"
else
	echo "inserting payload into bashrc"
	echo "Observer set up done: $OBSERVER_SETUP_DONE"
  cat /root/bashrc_payload.sh >> /root/.bashrc
fi
