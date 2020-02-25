#!/bin/bash

clear
echo -e "InsHack@ti's Butchery App\n"

if [[ ! -d "virtual_environment" ]]
then
    echo "Virtual environment folder does not exist!
Please run setup.sh to create the initial app's data."
    exit
fi

if [[ ! -d "instance" ]]
then
    echo "Instance folder does not exist!
Please run setup.sh to create the initial app's data."
    exit
fi

if [[ ! -d "uploads" ]]
then
    echo "Uploads folder does not exist!
Please run setup.sh to create the initial app's data."
    exit
fi

. virtual_environment/bin/activate

export FLASK_APP=butchery
export FLASK_ENV=development
flask run
