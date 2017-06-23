#
# ZFS commands abstracted in Python. Relies on Fabric to
# safely handle command execution and abstract SSH operations.
#
# We should never have come here.
#

from fabric.api import *
from voluptuous import Required, Schema


class Zfs:
    #
    # takes:    String <dataset_name>,  Dict <remote_host>, Boolean <is_remote>
    #
    def __init__(self, dataset_name, remote_host = None, is_remote = False):
        self.dataset_name = dataset_name
        self.is_remote = is_remote
        self.snapshot_name = None 
        if self.is_remote:
            self.remote_host = self._set_valid_remote_host(remote_host)

        # Do a bunch of logic to test the remote host?


    #
    # takes:    Dict <remote_host>
    #
    def _set_valid_remote_host(self, remote_host):
        # Define valid remote_host struct
        remote_host_schema = Schema({
            Required('host'): str,
            Required('port', default='22'): str,
            Required('user', default='root'): str,
            Required('keyfile', default='/root/.ssh/id_rsa'): str
        })

        # Validate passed-in remote_host struct
        try:
            valid_remote_host = remote_host_schema(remote_host)
        except:
            print "Invalid remote_host data structure"
            raise

        return valid_remote_host


    #
    # This assumes you have SSH keys
    #
    def _cmd_abstract(self, cmd):
        if self.is_remote:
            # Set necessary Fabric env vars for remote access
            env.host_string = self.remote_host['host']
            env.user = self.remote_host['user']
            env.key_filename = self.remote_host['keyfile']
            res = run(cmd)
        else:
            res = local(cmd,capture=True)

        return res


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
           
            returned = self._cmd_abstract('zfs list -r -H -o name ' + self.dataset_name + ' ' + snapshot_flag)
            
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
            snapshot = self._cmd_abstract('zfs snapshot ' + self.dataset_name + snapshot_name)
        
            # Use methods, rather than system calls to confirm
            confirm_snapshot = self.exists(self.dataset_name + snapshot_name, type_snapshot=True)
        
            if confirm_snapshot:
                self.snapshot_name = snapshot_name
                return True
            else:
                return False
    
    #
    # takes:    Object
    #
    # returns:  None
    #
    def send_recv(self, remote_zfs_host, incremental = False, previous_snapshot_name = None):
               
        ssh_host = remote_zfs_host.remote_host["host"]

        if incremental:
            self._cmd_abstract("zfs send -i " + self.dataset_name + previous_snapshot_name + " " + self.dataset_name + self.snapshot_name + " | ssh root@" + ssh_host + " zfs recv " + remote_zfs_host.dataset_name + self.snapshot_name)
        else:
            self._cmd_abstract("zfs send " + self.dataset_name + self.snapshot_name + " | ssh root@" + ssh_host + " zfs recv " + remote_zfs_host.dataset_name + self.snapshot_name)

    #
    # 
    #
    #
    #
    def delete_snapshot(self, snapshot_to_delete):
        
        self._cmd_abstract("zfs destroy " + snapshot_to_delete)
