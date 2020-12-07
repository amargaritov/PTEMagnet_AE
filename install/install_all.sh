#!/bin/bash -x 

# This fetches all needed files. 

#---------------------------------------------------------------

if [ -z "$1" ]
  then
    echo "Please set path where to put all data"
fi
INSTALL_PATH="$1"
mkdir -p $INSTALL_PATH || { echo "Can't create $INSTALL_PATH" ; exit 1; }
echo "Will install kernels to $INSTALL_PATH"

# directory containing this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

#---------------------------------------------------------------

export PTEM_ROOT="$INSTALL_PATH"

# get packages 
$SCRIPT_DIR/ubuntu_packages/restore.sh 

# get kernels 
export KERNEL_DIR="$INSTALL_PATH/linux"
$SCRIPT_DIR/kernel/build_kernels.sh $KERNEL_DIR 

# get vm_image
export IMAGE_DIR="$INSTALL_PATH/vm_images"
$SCRIPT_DIR/vm_disk_image/download_vm_disk_image.sh $IMAGE_DIR 
