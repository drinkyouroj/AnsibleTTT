#!/bin/bash
# Spin her up!
export LBNAME=$(cat elb.txt)
export KEYNAME=$(cat key_name.txt)
echo "Key Name: $KEYNAME"
python scripts/ec2_spin_up.py