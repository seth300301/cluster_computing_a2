#!/bin/bash

. ./openrc.sh; ansible-playbook -vv main.yaml | tee output.txt