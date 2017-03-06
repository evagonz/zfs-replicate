#!/usr/bin/env python

import os
import sys
import pytest
from fabric.api import *
from fabric.tasks import execute
from fabric.state import env, output

# Add to module search path
app_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_root + "/../lib")

import zfs


#
# Setup "fixture" for dependency injection in test methods
#
# Creates new dataset 'tank/zfsreptest.' Requires zpool tank to
# already exist.

@pytest.fixture(scope="session")
def zfs_instance():
    local('zfs create tank/zfsreptest')
    return zfs.Zfs("tank/zfsreptest")
    
    def fin():
        print ("teardown tank/zfsreptest")
        zfs_instance.close()
    request.addfinalizer(fin)
    return zfs_instance

#
# Zfs test class
#
class TestZfs:

    # Instance is correct type
    def test_zfs_instance(self, zfs_instance):
        assert isinstance(zfs_instance, zfs.Zfs)

    # List returns expected result
    def test_zfs_list(self, zfs_instance):
        assert zfs_instance.list() == ["tank/zfsreptest"]

    # Snapshot list returns expected result
    def test_zfs_list_snapshot(self, zfs_instance):
        assert zfs_instance.list(type_snapshot=True) == ["tank/snaps@20170207T1032"]

    # Snapshot take returns expected result 
    def test_zfs_snapshot(self, zfs_instance):
        assert zfs_instance.exists("tank/snaps@test", type_snapshot=True)

    # Snapshot does in fact exist
    def test_zfs_confirm_snapshot(self, zfs_instance):
        assert zfs_instance.snapshot("@test") == True


