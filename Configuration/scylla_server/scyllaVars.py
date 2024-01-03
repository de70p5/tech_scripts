scylla_config_file="/etc/scylla/scylla.yaml"

# variables for scylla.yaml file
scylla_default_data_dir="/var/lib/scylla/data"
scylla_default_work_dir="/var/lib/scylla"
scylla_default_commit_log_dir="/var/lib/scylla/commitlog"
scylla_default_hints_dir="/var/lib/scylla/hints"
scylla_default_view_hints_dir="/var/lib/scylla/view_hints"
scylla_new_data_dir="/data/ds/sdc/scylla/data"
scylla_new_work_dir="/data/ds/sdc/scylla"
scylla_new_commit_log_dir="/data/ds/sdc/scylla/commitlog"
scylla_new_hints_dir="/data/ds/sdc/scylla/hints"
scylla_new_view_hints_dir="/var/lib/scylla/view_hints"
scylla_cluster_name="eev-in-pod1a-ds-sdc"
scylla_listen_address="eev-in-pod1a-node01" #same for rpc,api addresses in scylla.yaml file
scylla_cluster_cluster_rackdc="eev-in-pod1a-ds-sdc-rack01"
scylla_authenticator="PasswordAuthenticator"
scylla_authorizer="CassandraAuthorizer"
scylla_file_snitch="GossipingPropertyFileSnitch"

# variables for /etc/scylla/cassandra-rackdc.properties
scylla_dc=""
scylla_rack=""
