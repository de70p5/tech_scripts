def return_op(command):
    cmd_op=subprocess.run(command,text=True,shell=True,check=True,capture_output=True)
    return cmd_op.stdout.strip()

node_private_ip=return_op("hostname -I")

def run_command(command):
    print(f"Running command: {command}")
    subprocess.run(command, shell=True, check=True)

def config_firewall_rules():
    run_command(f"sudo systemctl ufw enable ufw")
    run_command(f"sudo systemctl start ufw")
    for service in allowed_services:
        run_command(f"sudo ufw allow {service}")
    for port,comment in allowed_ports.items():
        run_command(f"sudo ufw allow {port} comment '{comment}'")
    print(f"Updated firewall rules\n current rules:\n\t{run_command('sudo ufw list')}")

def configure_hosts_file():
    for hostname in hostnames:
        run_command(f"echo $(hostname -I) {hostname}| sudo tee -a /etc/hosts")
    print(f"Updated file(/etc/hosts) is: \n {run_command('cat /etc/hosts')}")

def mysql_config():
    run_command(f"sudo systemctl stop mysql@bootstrap.service")
    # run_command(f"sudo sed -Ein 's+datadir=.*+datadir={mysql_new_data_dir}+' {mysql_conf_file}")
    run_command(f"sudo mkdir -p {mysql_new_data_dir}")
    # if do_backup:
    #     run_command(f"sudo cp -rdp {mysql_default_data_dir} /var/lib/mysql.bkp")        
    run_command(f"sudo cp -rdp {mysql_default_data_dir} {mysql_new_data_dir}")
    run_command(f"sudo chown -R mysql:mysql {mysql_new_data_dir}")
    run_command(f"sudo chown -R mysql:mysql /var/run/mysqld")

    data.replace("datadir=/var/lib/mysql",f"datadir={dataDirPath}")
    data.replace("wsrep_cluster_address=gcomm://",f"wsrep_cluster_address=gcomm://{wsrepClusterAddress}")
    data.replace("wsrep_cluster_name=pxc-cluster",f"wsrep_cluster_name={wsrepClusterName}")
    data.replace("#wsrep_node_address=",f"wsrep_node_address={wsrepNodeAddress}")
    data.replace("wsrep_node_name=pxc-cluster-node-1",f"wsrep_node_name={wsrepNodeName}")

    with open("/etc/mysql/mysql.conf.d/mysqld.cnf","w") as f:
        f.write(data)
        f.close()
    run_command(f"sudo systemctl status mysql.service")

def redpanda_config():
    run_command(f"sudo systemctl stop redpanda.service")
    # if do_backup:
    #     run_command(f"sudo cp -rdp {redpanda_default_data_dir} {redp}")
    run_command(f"sudo cp -rdp {redpanda_default_data_dir} {redpanda_new_data_dir}")  
    run_command(f"sudo chown -R redpanda:redpanda {redpanda_new_data_dir}")
    # run_command(f"sudo sed -iE 's+data_directory: /var/lib/redpanda/data+data_directory: {redpanda_new_data_dir}+' {redpanda_config_file}")
    # run_command(f"sudo sed -iE 's+coredump_dir: /var/lib/redpanda/coredump+coredump_dir: {redpanda_new_coredump_dir}+' {redpanda_config_file}")


    listConfContent=[{'redpanda': \
                    {'data_directory': {dataDirPath}, 'empty_seed_starts_cluster': True, 'seed_servers': [], \
                        'rpc_server': {'address': {rpcServerAddress}, 'port': 33145}, \
                        'kafka_api': [{'address': {kafkaApiAddress}, 'port': 9092}], \
                        'admin': [{'address': {adminAddress}, 'port': 9644}]}, \
                    'rpk': {'enable_usage_stats': True, 'tune_network': True, 'tune_disk_scheduler': True, 'tune_disk_nomerges': True, 'tune_disk_write_cache': True, 'tune_disk_irq': True, 'tune_cpu': True, 'tune_aio_events': True, 'tune_clocksource': True, 'tune_swappiness': True, 'coredump_dir': {coredumpDirPath}, 'tune_ballast_file': True}, \
                    'pandaproxy': {},\
                    'schema_registry': {}}]

    yaml_output = yaml.dump_all(listConfContent, sort_keys=False)

    try:
        with open("/etc/redpanda/redpanda.yaml", "w") as file:
            file.write(yaml_output)
    except IOError as e:
        print("Error writing to file:", e)
    run_command("systemctl status redpanda.service")

def scylla_config():
    # if do_backup:
    #     run_command(f"sudo cp -rdp {scylla_default_work_dir} {redp}")
    run_command(f"sudo cp -rdp {scylla_default_work_dir}/* {scylla_new_work_dir}")  
    run_command(f"sudo chown -R scylla:scylla {scylla_new_work_dir}")
    run_command(f"sudo sed -iE 's+\# workdir: {scylla_default_work_dir}+workdir: {scylla_new_work_dir}+' {scylla_config_file}")
    run_command(f"sudo sed -iE 's+\# data_file_directories:+data_file_directories:+' {scylla_config_file}")
    run_command(f"sudo sed -iE 's+\#    - {scylla_default_data_dir}+   - {scylla_new_data_dir}+' {scylla_config_file}")
    run_command(f"sudo sed -iE 's+\# commitlog_directory: {scylla_default_commit_log_dir}+commitlog_directory: {scylla_new_commit_log_dir}+' {scylla_config_file}")
    run_command(f"sudo sed -iE 's+\# hints_directory: {scylla_default_hints_dir}+hint_directory: {scylla_new_hints_dir}' {scylla_config_file}")
    run_command(f"sudo sed -iE 's+\# view_hints_directory: {scylla_default_hints_dir}+view_hint_directory: {scylla_new_hints_dir}' {scylla_config_file}")
    run_command(f"sudo sed -iE 's+\#cluster_name: .*+cluster_name: \'{scylla_cluster_name}\'' {scylla_config_file}")
    run_command(f"sudo sed -iE 's+\- seeds: .*+- seeds: \"{node_private_ip}\"' {scylla_config_file}")
    run_command(f"sudo sed -iE 's+listen_address: .*+listen_address: {node_hostname}' {scylla_config_file}")
    run_command(f"sudo sed -iE 's+rcp_address: .*+rpc_address: {node_hostname}' {scylla_config_file}")
    run_command(f"sudo sed -iE 's+api_address: .*+api_address: {node_hostname}' {scylla_config_file}")
    run_command(f"sudo sed -iE 's+\# authenticator: .*+authenticator: {scylla_authenticator}' {scylla_config_file}")
    run_command(f"sudo sed -iE 's+\# authorizer: .*+authorizer: {scylla_authorizer}' {scylla_config_file}")
    run_command(f"sudo sed -iE 's+\endpoint_snitch: .*+endpoint_snitch: {scylla_file_snitch}' {scylla_config_file}")
    run_command(f"systemctl status scylla-server")
    with open("/etc/scylla/cassandra-rackdc.properties","w") as file:
        file.write(data)
        file.close()
    data.replace("# dc=my_data_center",f"dc={scylla_dc}")
    data.replace("# rack=my_rack",f"rack={scylla_rack}")

def make_dirs():
    run_command(f"sudo mkdir -p {redpanda_new_data_dir} {mysql_new_data_dir} {scylla_new_work_dir}")