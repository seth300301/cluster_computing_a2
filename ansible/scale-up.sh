#!/bin/bash

. ./openrc.sh; ansible-playbook -vv -i inventory/inventory.ini --private-key=./shared-key.pem scale-up.yaml | tee output.txt
