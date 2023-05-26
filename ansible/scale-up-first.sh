#!/bin/bash

. ./openrc.sh; ansible-playbook -vv -i inventory/inventory.ini --private-key=./shared-key.pem scale-up-first.yaml | tee output.txt
