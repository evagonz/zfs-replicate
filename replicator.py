#!/usr/bin/env python
#
# Replicate all the things
#

import logging
from logging.config import dictConfig
#from fabric.api import *
#from fabric.tasks import execute
#from fabric.state import env, output
import os
#import libzfs_core
#import yaml
import sys

#
# Bootstrap
#
#app_root = os.path.dirname(os.path.abspath(__file__))
#config_path = os.path.join(app_root, 'conf/config.yml')
#if not os.path.isfile(config_path):
#    print "ERROR - Config file not found at: " + config_path + ". Exiting"
#    exit()


#
# Load config
#    TODO: Exit on failure
#with open(config_path, 'r') as ymlfile:
#    cfg = yaml.load(ymlfile)


#
# Get logger
#    TODO: Exit on failure
#logging.config.dictConfig(cfg['logging'])
#log = logging.getLogger('replicator_log')

#
# Variabe
#

if_snapshots = sys.argv[1]

#
# Functions
#
def __init__(dataset_name):
    self.dataset_name = dataset_name

def zfs_list(if_snapshots):
    
    returned_list = []
    if_snapshots = ""

    returned = local('zfs list -H -o name ' + self.dataset_name + ' ' + if_snapshots)

    for line in returned.splitlines():
        returned_list.append(line)

    return returned_list

#
# Main
#

returned_list = zfs_list(if_snapshots)


