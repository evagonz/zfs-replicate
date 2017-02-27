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
            res = local(cmd, capture=True)

        return res


    #
    # takes:    Boolean <snapshot>
    #
    # returns:  List
    #
    def list(self, snapshot = False):
        returned_list = []

        with quiet():
            snapshot_flag = "-t snapshot" if snapshot else ""

            returned = self._cmd_abstract('zfs list -r -H -o name ' + self.dataset_name + ' ' + snapshot_flag)

            for line in returned.splitlines():
                returned_list.append(line)

        return returned_list







