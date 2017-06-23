#!/usr/bin/env python
#
# Replicate all the things
#

"""ZFS Replicator

Usage:
  replicator.py <zfs_config>
  replicator.py (-h | --help)
  replicator.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""


from docopt import docopt
from fabric.api import *
from logging.config import dictConfig

import logging
import os
import sys
import yaml
import datetime

# Add to module search path
app_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_root + "/lib")

import zfs # TODO: This name sucks




def main():

    #
    # Bootstrap
    #
    config_path = os.path.join(app_root, 'conf/config.yml')
    if not os.path.isfile(config_path):
        print "ERROR - Config file not found at: " + config_path + ". Exiting"
        exit()

    # Load config
    #    TODO: Exit on failure
    with open(config_path, 'r') as logconffile:
        cfg = yaml.load(logconffile)

    # Get logger
    #    TODO: Exit on failure
    logging.config.dictConfig(cfg['logging'])
    log = logging.getLogger('replicator_log')
    log.info("ZFS REPLICATOR START");

    #
    # TODO: Consider ensuring that the user is root?
    #

    #
    # Use command-line yaml config file 
    #

    with open("replicator_config.yml", 'r') as zfsconffile:
        config = yaml.load(zfsconffile)
    
        print config['zfs_data']['local_dataset'] 

    #
    # Handle input using docopt
    #
    arguments = docopt(__doc__, version='Zfs Replicator 0.1')

    if not arguments['<zfs_config>'] :
        log.error("Missing mandatory YAML config file. Exiting.")
        sys.exit()
    else:
        zfs_config = arguments['<zfs_config>']

    #
    # Use command-line yaml config file 
    #

    with open(zfs_config, 'r') as zfsconffile:
        config = yaml.load(zfsconffile)

    #
    # Retrieve variables from config file
    #

    local_dataset_name = config['zfs_data']['local_dataset']
    remote_dataset_name = config['zfs_data']['remote_dataset']
    remote_host = config['zfs_data']['remote_host']    
    retain = config['zfs_data']['retain']

    #
    # Generate current & previous snapshot names
    #
    
    snapshot_name = datetime.datetime.now().strftime("@20%y%m%dT%H%M")
    previous_snapshot_name = "" 

    #
    # Work
    #

    local = zfs.Zfs(local_dataset_name)

    snapshot_list = local.list(type_snapshot=config['zfs_data']['type_snapshot'])
#    local.get_latest_snapshot(snapshot_list)
    local.snapshot(snapshot_name)
    

    for item in snapshot_list[0:-int(retain)]:
        snap_to_delete = item
        local.delete_snapshot(item)

    #remote = zfs.Zfs(remote_dataset_name, remote_host, is_remote = True)


#
# Return the correct log path based on current location
#
def get_log_name():
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, 'log/zfs_replicator.log')
    return logging.FileHandler(path)




if __name__ == '__main__':
        main()




