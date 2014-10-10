#!/bin/bash

#currently don't have multiple Load Balancers so I'm just setting this statically
export LBNAME=$(cat elb.txt)

if [[ "$1" == "A" ]]
then	
	export GROUP=A
elif [[ "$1" == "B" ]]
then
	export GROUP=B
else
	echo "Please define if we're changing to and updating to A or B"
	echo "Note, currently active group is:"
	python scripts/elb_current.py
	exit
fi

echo "Updating and changing to systems in group $1. If you're sure, press enter"
read

echo "Deregistering Current Group $1 instances (Should be Deregistered anyway)"
python scripts/elb_controls.py --dereg=1

echo "Updating Instances"
ansible-playbook -i scripts/ec2.py tasks/update_webservers.yml --private-key=private_key.pem

echo "Make sure the system is running okay first. Press enter when you're ready.  Here's the list of IPs and instance ids:"
python scripts/ec2.py
read

# Register the current group
python scripts/elb_controls.py

if [[ "$1" == "A" ]]
then
	export GROUP=B
	python scripts/elb_controls.py --dereg=1
elif [[ "$1" == "B" ]]
then
	export GROUP=A
	python scripts/elb_controls.py --dereg=1
fi