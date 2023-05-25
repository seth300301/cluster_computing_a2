#!/bin/bash

. ./openrc.sh; ansible-playbook -vv -i inventory/inventory.ini --private-key=./shared-key.pem run-first.yaml | tee output.txt
