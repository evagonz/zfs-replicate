#
# ZFS commands abstracted in Python. Relies on Fabric to 
# safely handle command execution and abstract SSH operations.
#
# We should never have come here. 
#

from fabric.api import *


class Zfs:
    #
    # takes:    String <dataset_name> 
    #
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name


    #
    # takes:    Boolean <type_snapshot>
    #
    # returns:  List
    #
    def list(self, type_snapshot = False):
        returned_list = []

        # Set command line arg for snapshot
        if type_snapshot:
            snapshot_flag = "-t snapshot"
        else:
            snapshot_flag = ""

        # Run list cmd & build return list
        with quiet():
            returned = local('zfs list -r -H -o name ' + self.dataset_name + ' ' + snapshot_flag, capture=True)
            for line in returned.splitlines():
                returned_list.append(line)

        return returned_list


    #
    # takes:    String <search_element>, Boolean <type_snapshot>
    #
    # returns:  Boolean
    #
    def exists(self, search_element, type_snapshot = False):
        # List all datasets for this dataset
        datasets = self.list(type_snapshot=type_snapshot)

        # See if the one we are looking for is there
        if search_element in datasets:
            return True
        else:
            return False


    #
    # takes:    None
    #
    # returns:  Boolean
    #
    def snapshot(self, snapshot_name):
        with quiet():
            # Take the shot
            snapshot = local('zfs snapshot ' + self.dataset_name + snapshot_name, capture=True)
        
            # Use methods, rather than system calls to confirm
            confirm_snapshot = self.exists(self.dataset_name + snapshot_name, type_snapshot=True)
        
            if confirm_snapshot:
                return True
            else:
                return False
        




