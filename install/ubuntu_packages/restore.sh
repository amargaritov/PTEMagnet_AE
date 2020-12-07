#!/bin/sh
 
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
pushd $SCRIPT_DIR
 
# packages
sudo apt-get install gnupg -y
tar xvf packages.tar.gz
sudo apt-key add Repo.keys
sudo cp -R sources.list* /etc/apt/
sudo apt-get update
sudo apt-get install dselect
sudo dselect update
sudo dpkg --set-selections < Package.list
sudo apt-get dselect-upgrade -y
sudo rm -rf Repo.keys sources.list* Package.list

popd
