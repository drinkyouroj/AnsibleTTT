#!/bin/bash
export GROUP=data
./ec2.py
ansible-playbook -i ec2.py tasks/restore_data.yml --private-key=~/.ssh/donkeykong69.pem -vvvv