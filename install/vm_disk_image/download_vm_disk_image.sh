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

echo "Downloading VM disk image..." 
wget --user=ftpuser --password=asplos21_8636909861 $LINK -O $INSTALL_PATH/rootfs.img
