#
# ZFS commands abstracted in Python. Relies on Fabric to 
# safely handle command execution and abstract SSH operations.
#
# We should never have come here. 
#

from fabric.api import *


class Zfs:

    #
    # takes:    String <dataset_name.
    #
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name


    #
    # takes:    Boolean <snapshot>
    #
    # returns:  List
    #
    def list(self, snapshot = False):
        returned_list = []

        with quiet():
            snapshot_flag = "-t snapshot" if snapshot else ""

            returned = local('zfs list -r -H -o name ' + self.dataset_name + ' ' + snapshot_flag, capture=True)

            for line in returned.splitlines():
                returned_list.append(line)

        return returned_list


