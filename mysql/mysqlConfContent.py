data="""# Template my.cnf for PXC
# Edit to your requirements.
[client]
socket=/var/run/mysqld/mysqld.sock

[mysqld]
server-id=1
datadir=/var/lib/mysql
socket=/var/run/mysqld/mysqld.sock
log-error=/var/log/mysql/error.log
pid-file=/var/run/mysqld/mysqld.pid

# Binary log expiration period is 604800 seconds, which equals 7 days
binlog_expire_logs_seconds=604800

######## wsrep ###############
# Path to Galera library
wsrep_provider=/usr/lib/galera4/libgalera_smm.so

# Cluster connection URL contains IPs of nodes
#If no IP is found, this implies that a new cluster needs to be created,
#in order to do that you need to bootstrap this node
wsrep_cluster_address=gcomm://

# In order for Galera to work correctly binlog format should be ROW
binlog_format=ROW

# Slave thread to use
wsrep_slave_threads=8

wsrep_log_conflicts

# This changes how InnoDB autoincrement locks are managed and is a requirement for Galera
innodb_autoinc_lock_mode=2

# Node IP address
#wsrep_node_address=192.168.70.63
# Cluster name
wsrep_cluster_name=pxc-cluster

#If wsrep_node_name is not specified,  then system hostname will be used
wsrep_node_name=pxc-cluster-node-1

#pxc_strict_mode allowed values: DISABLED,PERMISSIVE,ENFORCING,MASTER
pxc_strict_mode=ENFORCING

# SST method
wsrep_sst_method=xtrabackup-v2"""