from cqlConf import data
dc=""
rack=""
data.replace("# dc=my_data_center",f"dc={dc}")
data.replace("# rack=my_rack",f"rack={rack}")

with open("/etc/scylla/cassandra-rackdc.properties","w") as f:
    f.write(data)
    f.close()
