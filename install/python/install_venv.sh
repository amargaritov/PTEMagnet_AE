#!/bin/bash

pushd "$1"
if [ ! -d "./venv" ]; then 
	virtualenv -p /usr/bin/python venv
	source ./venv/bin/activate
	pip install glob2
  pip install scipy
  pip install pandas
	pip install 'fabric<2.0'

	pushd ./venv
	git clone https://github.com/marioskogias/distbenchr.git
	python ./distbenchr/setup.py install 
	popd

	deactivate 
else
	echo "Python venv already exixst. If you want to reinstall it please remove $1/venv dir and run this script again." 
fi
popd
