#!/bin/bash
#Motha Fuckin Rollback.

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

ansible-playbook -i scripts/ec2.py tasks/forgot_to_install_mbstring.yml --private-key=private_key.pem