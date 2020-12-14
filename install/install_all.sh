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

REPO_ROOT=$SCRIPT_DIR/..
echo "export REPO_ROOT=\"$REPO_ROOT\"" >> $REPO_ROOT/source.sh

#---------------------------------------------------------------

export PTEM_ROOT="$INSTALL_PATH"

# get packages 
$SCRIPT_DIR/ubuntu_packages/restore.sh 

# get kernels 
export KERNEL_DIR="$INSTALL_PATH/linux"
echo "export KERNEL_DIR=\"$INSTALL_PATH/linux\"" >> $REPO_ROOT/source.sh 
$SCRIPT_DIR/kernel/build_kernels.sh $KERNEL_DIR 

# get vm_image
export IMAGE_DIR="$INSTALL_PATH/vm_images"
echo "export IMAGE_DIR=\"$INSTALL_PATH/vm_images\"" >> $REPO_ROOT/source.sh 

$SCRIPT_DIR/vm_disk_image/download_vm_disk_image.sh $IMAGE_DIR 
if [ $? -eq 124 ]; then
    # Timeout occurred
  exit 124
fi

echo "$REPO_ROOT/evaluation/disable_thp_no_drop.sh" >> $REPO_ROOT/source.sh

# install venv
$SCRIPT_DIR/python/install_venv.sh $REPO_ROOT
echo "source $REPO_ROOT/venv/bin/activate" >> $REPO_ROOT/source.sh 

echo "cd $REPO_ROOT; source source.sh" >> ~/.bashrc 


source $REPO_ROOT/source.sh
