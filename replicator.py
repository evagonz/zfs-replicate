#!/usr/bin/env python
#
# Replicate all the things
#


import logging
from logging.config import dictConfig
import yaml
from fabric.api import *
import sys

#
# Bootstrap
#
app_root = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(app_root, 'conf/config.yml')
if not os.path.isfile(config_path):
    print "ERROR - Config file not found at: " + config_path + ". Exiting"
    exit()
#
# Load config
#    TODO: Exit on failure
with open(config_path, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
#
# Get logger
#    TODO: Exit on failure
logging.config.dictConfig(cfg['logging'])
log = logging.getLogger('replicator_log')

#
# Vars
#

dataset_name = sys.argv[1]

#
# Def
#

class Zrs:

    def __init__(self):
        self.dataset_name = dataset_name

    def list(self,snapshot):

        with quiet():
            returned_list = []
            if snapshot:
                snapshot = "-t snapshot"

	    returned = local('zfs list -r -H -o name ' + self.dataset_name + ' ' + snapshot, capture=True)

	    for line in returned.splitlines():
	        returned_list.append(line)

        return returned_list

#
# Main
#

ds_list = Zrs()
print ds_list.list("do it")

