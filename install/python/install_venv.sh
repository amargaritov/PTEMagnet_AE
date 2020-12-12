#!/bin/bash

pushd "$1"
virtualenv -p /usr/bin/python venv
source ./venv/bin/activate
pip install glob2
pip install 'fabric<2.0'

pushd ./venv
git clone https://github.com/marioskogias/distbenchr.git
python ./distbenchr/setup.py install 
popd

deactivate 
popd
