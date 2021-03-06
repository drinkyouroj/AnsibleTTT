#!/usr/bin/env python
#ec2_snapshots.py
import sys
import os
import argparse
import re
import time

import boto.ec2
import boto.ec2.elb
import boto.ec2.zone

import paramiko

from collections import defaultdict

class Ec2Snapshots(object):
	def __init__(self):
		'''Gets all the snapshots'''
		self.lbname = os.environ['LBNAME']
		self.keyname = os.environ['KEYNAME']
		self.ec2 = boto.ec2.connect_to_region("us-west-2")
		self.elb = boto.ec2.elb.connect_to_region("us-west-2")
		self.zones = self.ec2.get_all_zones()		

		self.chooseAMI()
		self.chooseSize()
		self.chooseSecurity()
		self.chooseGroup()
		self.chooseZone()

		self.spinHerUp()
		self.tagHerUp()

	def chooseAMI(self):
		images = self.ec2.get_all_images(owners=['self'])
		c = 0
		select_images = {}
		for image in images:
			c = c+1
			select_images[c] = image.id
			print c , str(image.name)

		choice = int(raw_input('Choose an image from below (the number that is):'))
		self.selected_ami = select_images[choice]

	def chooseSize(self):
		#let's just put in some defaults since we don't really want to use anything else right now
		types={1:'t2.small',2:'t2.medium',3:'m3.xlarge'}
		for k,v in types.iteritems():
			print k,str(v)

		choice = int(raw_input('Choose the size of instance:'))
		self.instance_type = types[choice]

	def chooseSecurity(self):
		groups = self.ec2.get_all_security_groups()
		c=0
		select_groups = {}
		for group in groups:
			c = c+1
			select_groups[c] = group.name
			print c, str(group.name)
		choice = int(raw_input('Choose the security group:'))
		self.security_group = select_groups[choice]
		print self.security_group

	#This Group is the A or B running set group.
	def chooseGroup(self):
		group = 'x'
		while group not in ('A','B'):
			group = raw_input('Choose the Group (A or B):')
			print group

		self.group = group

	def chooseZone(self):
		c=0
		select_zones = {}
		for zone in self.zones:
			c=c+1
			select_zones[c] = zone.name
			print c, str(zone.name)
		choice = int(raw_input('Choose your availability Zones wisely:'))
		self.availability_zone = select_zones[choice]

	def spinHerUp(self):
		self.new_instance = self.ec2.run_instances(
									image_id=self.selected_ami,
									min_count=1,
									max_count=1,
									key_name=self.keyname,
									security_groups=[self.security_group],
									instance_type=self.instance_type,
									placement=self.availability_zone
									)

	def tagHerUp(self):
		instance = self.new_instance.instances[0]
		print instance.id
		status = instance.update()
		while status == 'pending':
			time.sleep(10)
			status = instance.update()

		if status == 'running':
			instance.add_tag('Group', self.group)
			instance.add_tag('Name', 'WebServer')
			retry = True
			while retry:
				try:
					instance.update()
					if len(instance.ip_address) > 0:
						print instance.ip_address
						retry = False
				except:
					time.sleep(10)
			
			print "1 Yes"
			print "2 No"
			choice = int(raw_input('Do you want to attach this to the LoadBalancer?:'))
			if choice == 2:
				print 'Not attached'
			elif choice == 1:
				self.elb.register_instances(self.lbname,[instance.id])





Ec2Snapshots()