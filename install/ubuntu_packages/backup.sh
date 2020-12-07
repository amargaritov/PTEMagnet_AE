#!/bin/sh
 
# packages                                                                      
dpkg --get-selections > Package.list
sudo cp -R /etc/apt/sources.list* .
sudo apt-key exportall > Repo.keys
tar cvfz packages.tar.gz Package.list sources.list* Repo.keys
sudo rm -rf Package.list Repo.keys sources.list*
