#!/bin/bash

if [[ "$1" == "A" ]]
then	
	export GROUP=A
elif [[ "$1" == "B" ]]
then
	export GROUP=B
else
	echo "Please define if we're updating A or B"
	exit
fi

echo "Updating systems in group $1. If you're sure, press enter"
read

echo "Deregistering Current Group $1 instances"
python elb_controls.py --dereg=1


echo "Updating Instances"
ansible-playbook -i ec2.py tasks/update_webservers.yml --private-key=~/.ssh/donkeykong69.pem

echo "Make sure the system is running okay first. Press enter when you're ready.  Here's the list of IPs and instance ids:"
python ec2.py
read

# Register the current group
python elb_controls.py

if [[ "$1" == "A" ]]
then
	export GROUP=B
	python elb_controls.py --dereg=1
elif [[ "$1" == "B" ]]
then
	export GROUP=A
	python elb_controls.py --dereg=1
fi