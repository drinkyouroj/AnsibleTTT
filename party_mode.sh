#!/bin/bash
#WTF is a party mode?  Its where we put up every web instance A or B and just go like hell.

export LBNAME=LB1

echo "Please define if we're changing to and updating to A or B"
echo "Note, currently active group is:"
export current=$(python scripts/elb_current.py)
echo "$current"

if [[ "$current" == "A" ]]
then
	export GROUP=B
elif [[ "$current" == "B" ]]
then
	export GROUP=A
fi

echo "Do you want to update the other group $GROUP before going live?"
echo "Yes/No"
read answer

if [[ "$answer" == "Yes" ]]
then
	ansible-playbook -i scripts/ec2.py tasks/update_webservers.yml --private-key=~/.ssh/donkeykong69.pem
fi

echo "Group $GROUP going up"
python scripts/elb_controls.py