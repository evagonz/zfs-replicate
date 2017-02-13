#!/usr/bin/env python

import os
import sys
import pytest

# Add to module search path
app_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_root + "/../lib")

import zfs


#
# Setup "fixture" for dependency injection in test methods
#
# Requires a zpool "tank/snaps". As we complete various methods
# we can start by controlling the build of the necessary test 
# environment here. For example, creating a known zpool first, 
# or creating a snapshot by a known name.
#
@pytest.fixture
def zfs_instance():
    return zfs.Zfs("tank/snaps")


#
# Zfs test class
#
class TestZfs:

    # Instance is correct type
    def test_zfs_instance(self, zfs_instance):
        assert isinstance(zfs_instance, zfs.Zfs)

    # List returns expected result
    def test_zfs_list(self, zfs_instance):
        assert zfs_instance.list() == ["tank/snaps"]

    # Snapshot list returns expected result
    def test_zfs_list_snapshot(self, zfs_instance):
        assert zfs_instance.list(snapshot=True) == ["tank/snaps@20170207T1032"]



        
