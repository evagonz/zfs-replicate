#!/usr/bin/env python
#
# Replicate all the things
#

from fabric.api import *
import logging
from logging.config import dictConfig
import os
import sys
import yaml

# Add to module search path
app_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_root + "/lib")

import zfs # TODO: This name sucks




#
# Bootstrap
#
config_path = os.path.join(app_root, 'conf/config.yml')
if not os.path.isfile(config_path):
    print "ERROR - Config file not found at: " + config_path + ". Exiting"
    exit()

# Load config
#    TODO: Exit on failure
with open(config_path, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

# Get logger
#    TODO: Exit on failure
logging.config.dictConfig(cfg['logging'])
log = logging.getLogger('replicator_log')




#
# Handle input
#

if len(sys.argv) < 2:
    log.error("Missing mandatory argument dataset_name. Exiting.")
    sys.exit()
else:
    dataset_name = sys.argv[1]




#
# Main
# TODO: These should essentially become unit tests
#
zfs_test = zfs.Zfs(dataset_name)

# Dataset
print zfs_test.list()

# Snapshot
print zfs_test.list(snapshot=True)












