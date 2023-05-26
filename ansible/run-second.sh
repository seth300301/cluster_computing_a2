#!/bin/bash

ansible-playbook -vv -i inventory/inventory.ini --private-key=./shared-key.pem run-second.yaml | tee output.txt
