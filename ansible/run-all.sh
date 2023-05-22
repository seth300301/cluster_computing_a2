#!/bin/bash

. ./openrc.sh; ansible-playbook -vv -i inventory/inventory.ini main.yaml | tee output.txt
