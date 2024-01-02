from mysqlConfContent import data

dataDirPath=""
wsrepClusterAddress=""
wsrepClusterName=""
wsrepNodeAddress=""
wsrepNodeName=""

data.replace("datadir=/var/lib/mysql",f"datadir={dataDirPath}")
data.replace("wsrep_cluster_address=gcomm://",f"wsrep_cluster_address=gcomm://{wsrepClusterAddress}")
data.replace("wsrep_cluster_name=pxc-cluster",f"wsrep_cluster_name={wsrepClusterName}")

data.replace("#wsrep_node_address=",f"wsrep_node_address={wsrepNodeAddress}")
data.replace("wsrep_node_name=pxc-cluster-node-1",f"wsrep_node_name={wsrepNodeName}")

with open("/etc/mysql/mysql.conf.d/mysqld.cnf","w") as f:
    f.write(data)
    f.close()
