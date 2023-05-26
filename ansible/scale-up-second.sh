#!/bin/bash

./openrc.sh; ansible-playbook -vv -i inventory/inventory.ini --private-key=./shared-key.pem scale-up-second.yaml | tee output.txt
