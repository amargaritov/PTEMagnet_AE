#!/bin/bash -x 

# This script build clean and modified kernels.

#---------------------------------------------------------------

if [ -z "$1" ]
  then
    echo "Please set path where to install the kernels"
fi
INSTALL_PATH="$1"
mkdir -p $INSTALL_PATH || { echo "Can't create $INSTALL_PATH" ; exit 1; }
echo "Will install kernels to $INSTALL_PATH"

# directory containing this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

#---------------------------------------------------------------

# $1 - INSTALL_PATH
# $2 - tag of linux dir 
function prepare_repo() { 
  TARGET_DIR="$1"/linux_"$2"
  echo "Loading kernel sources from Github for $2 kernel..."
  # download kernel sources
  git clone git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git $TARGET_DIR
  pushd $TARGET_DIR
  # set kernel version to 4.19
  git checkout v4.19
  # setup config
  cp $SCRIPT_DIR/kernel_config $TARGET_DIR/arch/x86/configs/x86_64_defconfig
  popd
}

# $1 - INSTALL_PATH
# $2 - tag of linux dir 
function patch_kernel() { 
  TARGET_DIR="$1"/linux_"$2"
  pushd $TARGET_DIR
  # apply patch to get atc_idea memory reservation
  git apply $SCRIPT_DIR/kernel_patch
  popd
}

# $1 - INSTALL_PATH
# $2 - tag of linux dir 
function build_image() {
  TARGET_DIR="$1"/linux_"$2"
  echo "Building $2 kernel..."
  pushd $TARGET_DIR
  make ARCH=x86 defconfig
  # build kernel
  make -j bzImage 
  popd
}

#---------------------------------------------------------------

# 1. Build clean kernel 

prepare_repo $INSTALL_PATH clean
build_image  $INSTALL_PATH clean

# 2. Build modified kernel 

prepare_repo $INSTALL_PATH modified
patch_kernel $INSTALL_PATH modified
build_image  $INSTALL_PATH modified
