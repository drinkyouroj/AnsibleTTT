#!/bin/bash
export GROUP=data
python scripts/ec2.py
ansible-playbook -i scripts/ec2.py tasks/restore_data.yml --private-key=~/.ssh/donkeykong69.pem -vvvv