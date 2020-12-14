#!/bin/bash

if [ -z "$1" ]
  then
    echo "Please set path where to save the VM disk image"
fi

# This script build clean and modified kernels.

#---------------------------------------------------------------

INSTALL_PATH="$1"
mkdir -p $INSTALL_PATH || { echo "Can't create $INSTALL_PATH" ; exit 1; }
echo "Will install the VM disk image to $INSTALL_PATH"

# directory containing this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

#---------------------------------------------------------------

LINK="$(cat $SCRIPT_DIR/vm_image_link)"

if [ -z "$(hostname | grep cloudlab)" ]; then 
	# if we are not on Cloudlab we need to download a disk 
  echo "Downloading VM disk image..." 
  wget --timeout=30 --tries=2 --user=ftpuser --password=asplos21_8636909861 $LINK:/root.img -O $INSTALL_PATH/rootfs.img
	if [ $? -eq 4 ]; then
	    # Timeout occurred
    wget --timeout=30 --tries=2 --user=ftpuser --password=asplos21_8636909861 $LINK:/root.img.gz -O $INSTALL_PATH/rootfs.img.gz
    if [ $? -eq 4 ]; then
        # Timeout occurred
      echo "It seems that something is wrong with the download source. Please sent a message to Artemiy <artemiy.margaritov@ed.ac.uk>" 
      exit 124
    else 
      echo "Unpacking..."
      pigz -d $INSTALL_PATH/rootfs.img.gz
    fi
	fi
# else 
# Cloudlab already has a preinstalled disk
fi


