#!/bin/bash
export GROUP=B
ansible-playbook -i ec2.py tasks/update_webservers.yml --private-key=~/.ssh/donkeykong69.pem