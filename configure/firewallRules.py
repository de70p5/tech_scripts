#firewall_vars
allowed_services=['ssh','http','https']
redpanda_ports={"33145/tcp":"Redpanda RPC","9092/tcp":"Redpanda API","8082/tcp":"Redpanda Proxy","8081/tcp":"Redpanda Schema Registry","9644/tcp":"Redpanda Prometheus"}
scylladb_ports={"9042/tcp":"ScyllaDB RPC","9142/tcp":"ScyllaDB RPC Secure","7000/tcp":"ScyllaDB API","7001/tcp":"ScyllaDB API Secure","7199/tcp":"ScyllaDB Internal",
                "10000/tcp":"ScyllaDB REST","9180/tcp":"ScyllaDB Utility","9100/tcp":"ScyllaDB Utility","9160/tcp":"ScyllaDB Utility","19042/tcp":"ScyllaDB Utility",
                "19142/tcp ":"ScyllaDB utility"}
tomcat_ports={"8181/tcp":"Tomcat API or API","8282/tcp":"Tomcat API or API","8383/tcp":"Tomcat API or API","8484/tcp":"Tomcat API or API","8585/tcp":"Tomcat API or API"}
mysql_ports={"4444/tcp":"MySQL Utility","3306/tcp":"MySQL Utility","4567/tcp":"MySQL Utility","4567/udp":"MySQL Utility","4568/tcp":"MySQL Utility"}
allowed_ports={}
allowed_ports=allowed_ports|redpanda_ports|scylladb_ports|tomcat_ports|mysql_ports