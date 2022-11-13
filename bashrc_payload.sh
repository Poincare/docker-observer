# This function is used to check in files that we should copy
# from the container into a local directory at shell exit.
function checkin() 
{
	CHECKED_IN_FILE_PATH=$(realpath $1)
	echo $CHECKED_IN_FILE_PATH >> /root/observer_checked_in_files.txt	
	echo "Checked in $CHECKED_IN_FILE_PATH" 
}

export OBSERVER_SETUP_DONE="1"
trap 'x=$?; echo "OUTPUT: $x" >> /root/observer_log.txt; history 1 >> /root/observer_log.txt; ' DEBUG
