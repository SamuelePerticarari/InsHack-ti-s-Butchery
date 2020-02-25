#!/bin/bash

clear
echo -e "InsHack@ti's Butchery App Setup\n"

if [[ -d "virtual_environment" ]]
then
    echo -n "Virtual environment folder already exists.
Would you like to re-create it? [y/n]: "
    while true; do
        read yn
        case ${yn} in
            [Yy]* )
                rm -r virtual_environment
                echo
                virtualenv virtual_environment
                echo
                echo "Virtual environment folder re-created.";
                break;;
            [Nn]* )
                break;;
            * )
                echo -n "Please answer yes or no. ";;
        esac
    done
else
    virtualenv virtual_environment
    echo
    echo "Virtual environment folder created."
fi

. virtual_environment/bin/activate
echo
pip install -r requirements.txt

export FLASK_APP=butchery
export FLASK_ENV=development

if [[ -d "instance" ]]
then
    echo
    echo -n "Instance folder already exists.
Would you like to re-create it? (please be aware that this will erase all database data) [y/n]: "
    while true; do
        read yn
        case ${yn} in
            [Yy]* )
                rm -r instance
                echo
                flask init-db
                break;;
            [Nn]* )
                break;;
            * )
                echo -n "Please answer yes or no. ";;
        esac
    done
else
    echo
    flask init-db
fi

if [[ -d "uploads" ]]
then
    echo
    echo -n "Uploads folder already exists.
Would you like to re-create it? (please be aware that this will erase all uploaded files) [y/n]: "
    while true; do
        read yn
        case ${yn} in
            [Yy]* )
                rm -r uploads
                mkdir uploads
                echo
                echo "Uploads folder re-created."
                break;;
            [Nn]* )
                break;;
            * )
                echo -n "Please answer yes or no. ";;
        esac
    done
else
    mkdir uploads
    echo
    echo "Uploads folder created."
fi

echo
echo "Initial setup completed."