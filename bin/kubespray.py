#!/usr/bin/env python

__version__ = '0.1'

import sys
import yaml
import logging
import os
import time
import re
import argparse
from pprint import pprint
from termcolor import colored
#import kubespray.prepare
#import kubespray.deploy
#import kubespray.info

class Colors:
        info = colored('Info :', 'green', attrs=['bold'])
        warning = colored('Warning :', 'yellow', attrs=['bold'])
        error = colored('Error :', 'red', attrs=['bold'])

class KubeSpray:
    """
    Command line wrapper on top of Ansible which helps to deploy a kubernetes cluster
    """

    def __init__(self, config_file):
        self.config_file = config_file
        if self.config_file is None:
            self.config_file = "/etc/kubespray/kubespray.yml"

        self.loglevel = None
        self.logfile = None

        # logging setting
        self.logger = logging.getLogger()
        self.hdlr1 = logging.FileHandler(self.logfile)
        self.formatter_log = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.hdlr1.setFormatter(self.formatter_log)
        self.logger.addHandler(self.hdlr1)
        self.logger.setLevel(getattr(logging, self.loglevel.upper()))

    def configure():
        """
        Retrieve configuration parameters from the config_file
        """
        self.logger.debug('configuration file : %s' % self.config_file)
        if self.config_file:
            try:
                with open(self.config_file, "r") as f:
                    config = yaml.load(f)
            except:
                print("%s Can't read configuration file %s." % (Colors.error, self.config_file))
                sys.exit(1)
    
            self.inventory_path = config.get('inventory_path', self.inventory_path)
            self.logfile = config.get('logfile', self.logfile)
            self.loglevel = config.get('loglevel', self.loglevel)
        else:
            print("%s Config file is None !!!!" % Colors.error)
            sys.exit(1)

    def query_yes_no(self, question, default="yes"):
        """Question user input 'Yes' or 'No'"""
        valid = {"yes":True, "y":True, "no":False, "n":False}
        if default == None:
          prompt = " [y/n] "
        elif default == "yes":
          prompt = " [Y/n] "
        elif default == "no":
          prompt = " [y/N] "
        else:
          raise ValueError("%s invalid default answer: '%s'" % (Colors.error, default))
        while True:
            sys.stdout.write(question + prompt)
            choice = raw_input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("%s Please answer with 'yes' or 'no' (or 'y' or 'n').\n" % Colors.warning)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='kubespray', description='%(prog)s Kubernetes cluster deployment tool')

    subparsers = parser.add_subparsers(help='commands')

    # prepare
    prepare_parser = subparsers.add_parser('prepare', help='generate inventory and create vms on cloud providers')
    prepare_parser.add_argument('--nodes', dest='k8s_nodes', metavar='N', nargs='+', help='List of nodes')
    prepare_parser.add_argument('--masters', dest='k8s_masters',metavar='N', nargs='+', help='List of masters')
    prepare_parser.add_argument('--coreos', default=False, action='store_true', help='bootstrap python on CoreOS')
    
    # aws
    aws_parser = subparsers.add_parser('aws', help='Create AWS instances and generate inventory')
    aws_parser.add_argument('--access_key', dest='aws_access_key', help='AWS access key')
    aws_parser.add_argument('--secret_key', dest='aws_secret_key', help='AWS secret key')
    aws_parser.add_argument('--type', dest='instance_type', help='AWS instance type')
    aws_parser.add_argument('--ami', dest='aws_ami', help='AWS AMI')
    aws_parser.add_argument('--nodes', dest='k8s_nodes', type=int, help='Number of nodes')
    aws_parser.add_argument('--masters', dest='k8s_masters', type=int, help='Number of masters')
    aws_parser.add_argument('--coreos', default=False, action='store_true', help='bootstrap python on CoreOS')

    # gce
    gce_parser = subparsers.add_parser('gce', help='Create GCE machines and generate inventory')
    gce_parser.add_argument('--sshkey', dest='gce_sshkey_path', help='GCE ssh key path')
    gce_parser.add_argument('--zone', dest='gce_zone', help='GCE zone')
    gce_parser.add_argument('--type', dest='gce_machine_type', help='GCE machine type')
    gce_parser.add_argument('--image', dest='gce_image', help='GCE image')
    gce_parser.add_argument('--nodes', dest='k8s_nodes', type=int, help='Number of nodes')
    gce_parser.add_argument('--masters', dest='k8s_masters', type=int, help='Number of masters')
    gce_parser.add_argument('--coreos', default=False, action='store_true', help='bootstrap python on CoreOS')

    # deploy
    deploy_parser = subparsers.add_parser('deploy', help='Create GCE machines and generate inventory')
    deploy_parser.add_argument('--network-plugin', choices=['flannel', 'weave', 'calico'])
    deploy_parser.add_argument('--aws', default=False, action='store_true', help='Kubernetes deployment on AWS')
    deploy_parser.add_argument('--gce', default=False, action='store_true', help='Kubernetes deployment on GCE')
    deploy_parser.add_argument('--upgrade', default=False, action='store_true', help='Upgrade Kubernetes cluster')
    deploy_parser.add_argument('--ansible_opts', dest='ansible_opts', metavar='N', nargs='+', help='Ansible options')

    # cluster-info
    parser.add_argument('cluster-info', default=False, action='store_true', help='Display information on a running cluster')
    
    result = parser.parse_args()
    print(result)
    #arguments = dict(result._get_kwargs())
    #print(arguments)
