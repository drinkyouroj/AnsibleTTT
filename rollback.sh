#!/bin/bash
#Motha Fuckin Rollback.

export LBNAME=$(cat elb.txt)

echo "Rollin Rollin Roll back"
echo "Note, currently active group is:"
python scripts/elb_current.py

echo "So, which Group are we rolling back to? (Currently A or B)"
read group

export GROUP=$group
echo "Below instances will come alive.  Hit enter to continue:"
python scripts/ec2.py
read

#register the new Group
python scripts/elb_controls.py

#de-register the other group
if [[ "$group" == "A" ]]
then
	export GROUP=B
	python scripts/elb_controls.py --dereg=1
elif [[ "$group" == "B" ]]
then
	export GROUP=A
	python scripts/elb_controls.py --dereg=1
fi