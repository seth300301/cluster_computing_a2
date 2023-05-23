#!/bin/bash

. ./openrc.sh; ansible-playbook -vv -i inventory/inventory.ini --private-key=./shared-key.pem run-all.yaml | tee output.txt
