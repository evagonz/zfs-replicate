#!/usr/bin/env python
#
# Replicate all the things
#

import logging
from logging.config import dictConfig
from fabric.api import *
from fabric.tasks import execute
from fabric.state import env, output
import os
import libzfs_core
import yaml


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
# Test function using Fabric
#
def dataset_exists(dataset):
    
    ret_list = []

    try:
        # Fabric context to silence verbose messages
        # and not abort on command failure
        with quiet():
            ret = local('zfs list -H -o name ' + dataset, capture=True)

        # Build output struct
        for line in ret.splitlines():
            ret_list.append(line)

        # Struct should contain exactly one line and match
        # the input dataset name
        if len(ret_list) == 1 and dataset == ret_list[0]:
            return True

    except FabricException:
        return False




#
# Main
#
if dataset_exists("tank/test_dataset_1"):
    log.info("FOUND DATASET")
else:
    log.error("DATASET NOT FOUND")





