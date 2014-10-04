#!/bin/bash
export GROUP=A
ansible-playbook -i ec2.py tasks/update_webservers.yml --private-key=~/.ssh/donkeykong69.pem