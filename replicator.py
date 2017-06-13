#!/usr/bin/env python
#
# Replicate all the things
#

"""ZFS Replicator

Usage:
  replicator.py <dataset_name> <snapshot_name> 
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
    with open(config_path, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    # Get logger
    #    TODO: Exit on failure
    logging.config.dictConfig(cfg['logging'])
    log = logging.getLogger('replicator_log')
    log.info("ZFS REPLICATOR START");

    #
    # TODO: Consider ensuring that the user is root?
    #




    #
    # Handle input using docopt
    #
    arguments = docopt(__doc__, version='Zfs Replicator 0.1')

    #if not arguments['<dataset_name>', '<snapshot_name>'] :
    #    log.error("Missing mandatory argument <dataset_name> and/or <snapshot_name>. Exiting.")
    #    sys.exit()
    #else:
    dataset_name = arguments['<dataset_name>']
    snapshot_name = arguments['<snapshot_name>']




    #
    # TODO: These should essentially become unit tests
    #
    zfs_test = zfs.Zfs(dataset_name)

    # Dataset
    print zfs_test.list()

    # Snapshot
    print zfs_test.list(type_snapshot=True)

    # Take snapshot
    print zfs_test.snapshot(snapshot_name)

    # Send snapshot (eventually)
    remote_test = zfs.Zfs("tank/test_dataset_4", remote_host={ 'host': '172.27.6.148'}, is_remote=True)

    zfs_test.send_recv(remote_test, incremental=True, previous_snapshot_name="@20170613T1250")


#
# Return the correct log path based on current location
#
def get_log_name():
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, 'log/zfs_replicator.log')
    return logging.FileHandler(path)




if __name__ == '__main__':
        main()




