#!/usr/bin/env python
#This is based on the EC2 inventory script provided with Ansible.
import sys
import os
import argparse
import re

from time import time
import boto.ec2
from collections import defaultdict

try:
    import json
except ImportError:
    import simplejson as json

class Ec2Group(object):
    def __init__(self):
        ''' Where the magic begins '''
        #set inventory
        self.parse_cli_args()
        self.group = os.environ['GROUP']
        self.get_servers()


    def get_servers(self):
        conn = boto.ec2.connect_to_region("us-west-2")
        self.parse_cli_args()
        self.hosts = {'ec2': [], 'ec2_instance':[]}

        reservations = conn.get_all_instances()
        for res in reservations:
            for inst in res.instances:
                if 'Group' in inst.tags and inst.tags['Group'] == self.group:
                   #print vars(inst)
                    self.hosts['ec2'].append(str(inst.ip_address))
                    self.hosts['ec2_instance'].append(str(inst.id))

        print json.dumps(self.hosts, sort_keys=True, indent=2)

    def parse_cli_args(self):
        parser = argparse.ArgumentParser(description='List by groups')
        parser.add_argument('--list', action='store_true', default=True,
                           help='List instances (default: True)')
        self.args = parser.parse_args()

Ec2Group()