#!/usr/bin/env python
#
# Replicate all the things
#

from fabric.api import *
import sys

#
# Def
#

dataset_name = sys.argv[1]

class Zrs:

    def __init__(self):
        self.dataset_name = dataset_name

    def list(self):

        with quiet():
            returned_list = []

	    returned = local('zfs list -H -o name ' + self.dataset_name, capture=True)

	    for line in returned.splitlines():
	        returned_list.append(line)

        return returned_list

ds_list = Zrs()
print ds_list.list()

