#!/usr/bin/env python
#Find the current group attached to the LB.

import sys
import os
import argparse
import re

from time import time
import boto.ec2
import boto.ec2.elb
from collections import defaultdict

class ElbCurrent(object):
    def __init__(self):
        ''' Where the magic begins '''

        #set inventory
        self.lbname = os.environ['LBNAME']

        #its all the same to here.
        elb = boto.ec2.elb.connect_to_region('us-west-2')
        load_balancer = elb.get_all_load_balancers([self.lbname])[0]
        instance_ids = [instance.id for instance in load_balancer.instances]

        ec2 = boto.ec2.connect_to_region("us-west-2")
        reservations = ec2.get_all_instances(instance_ids)
        tags = [i.tags['Group'] for r in reservations for i in r.instances]
        first = tags[0]
        print  first

        #check to see if the current situation is bad. (mixed between group A and B for whatever reason.)
        for tag in tags:
            if tag != first:
                print "The instnaces have become mixed between A and B, be sure to take care of that through the AWS console before continuing."
            

ElbCurrent()