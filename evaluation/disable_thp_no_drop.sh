#!/bin/bash 

CUR_DIR=$(pwd)

display_usage() { 
echo -e "\nUsage: [install_path]\n" 
} 

check_if_succeeded() {
	if [ $? -eq 0 ]; then
	    echo OK
	else
	    echo FAIL
	    exit 1
	fi
}


prepare_system() {
	echo "Disable THP..."

  sudo sh -c "echo 'never' > /sys/kernel/mm/transparent_hugepage/enabled"
  sudo sh -c "echo 'never' > /sys/kernel/mm/transparent_hugepage/defrag"

#	echo "Drop OS caches..."
#	sudo sync; 
#  sudo sh -c "echo '3' > /proc/sys/vm/drop_caches"
}

prepare_system

