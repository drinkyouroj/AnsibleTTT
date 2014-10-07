#!/usr/bin/env python
#This is based on the EC2 inventory script provided with Ansible.
#I'm starting to hate ansible more and more. Why not just use boto?
import sys
import os
import argparse
import re

from time import time
import boto.ec2
import boto.ec2.elb
from collections import defaultdict

try:
    import json
except ImportError:
    import simplejson as json

class Ec2Controls(object):
    def __init__(self):
        ''' Where the magic begins '''
        self.parse_cli_args()

        #set inventory
        self.group = os.environ['GROUP']
        self.lbname = os.environ['LBNAME']
        self.get_servers()
        
        #its all the same to here.
        elb = boto.ec2.elb.connect_to_region('us-west-2')
        if self.args.dereg:
            for instance in self.hosts['ec2_instances']:
                elb.deregister_instances(self.lbname,instance)
                print('De-Registered '+ instance)
        else:
            for instance in self.hosts['ec2_instances']:
                elb.register_instances(self.lbname,instance)
                print('Registered '+ instance)

    def get_servers(self):
        conn = boto.ec2.connect_to_region("us-west-2")
        self.hosts = {'ec2': [], 'ec2_instances':[]}

        reservations = conn.get_all_instances()
        for res in reservations:
            for inst in res.instances:
                if 'Group' in inst.tags:
                    if inst.tags['Group'] == self.group:
                        self.hosts['ec2_instances'].append(str(inst.id))

        #print json.dumps(self.hosts, sort_keys=True, indent=2)

    def parse_cli_args(self):
        parser = argparse.ArgumentParser(description='Register or Dereg?')
        parser.add_argument('--dereg', action='store', default=False,
                           help='Deregister Instances (default: False)')
        self.args = parser.parse_args()

Ec2Controls()