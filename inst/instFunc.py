import subprocess
from vars import *
from serviceFileContents import *
from confContents import *
from errorContents import *
from credentials import *
from redpandaRepoCont import *

def set_hostname():
    run_command(f"sudo hostnamectl set-hostname {hostname}")

def run_command(command):
    print(f"Running command: {command}")
    subprocess.run(command, shell=True, check=True)


def install_java():
    run_command(f"curl -L '{jdk_file_url}' > {jdk_file_name}")
    run_command(f"sudo mkdir -p {java_installation_path}")
    run_command(f"sudo tar -xzvf {jdk_file_name} -C /usr/java")
    run_command(f'echo \'export PATH=$PATH:{java_home_path}/bin\' >> ~/.bashrc')
    run_command(f'echo \'export JAVA_HOME={java_home_path}\' >> ~/.bashrc')
    #run_command(f"sudo ln -s /usr/java/jdk-{jdk_version}/bin/java /usr/bin/java")
    
def install_maven():
    run_command(f"curl -L '{maven_url}' > {maven_file_name}")
    run_command(f"sudo tar -xvzf {maven_file_name} -C /opt")
    run_command(f"echo \'export PATH=$PATH:{maven_file_save_path}/apache-maven-{maven_version}/bin\' >> ~/.bashrc")
    run_command(f"echo \'export M2_HOME={maven_file_save_path}/apache-maven-{maven_version}\' >> ~/.bashrc")
    run_command(f"echo \'export M2={maven_file_save_path}/apache-maven-{maven_version}/bin\' >> ~/.bashrc")
    
def install_tomcat():
    run_command(f"curl -L '{tomcat_url}' > {tomcat_file_name}")
    run_command(f"sudo mkdir -p {tomcat_base_installation_path} || echo \"Tomcat dir is created\"")
    run_command(f"sudo tar -xvzf {tomcat_file_name} -C {tomcat_base_installation_path}")
    run_command(f"sudo cp -rdp {tomcat_base_installation_path}/apache-tomcat-9.0.84/* {tomcat_base_installation_path}")
    run_command(f"sudo rm -rf {tomcat_base_installation_path}/apache-tomcat-9.0.84")
    run_command(f"sudo useradd -m -d {tomcat_base_installation_path} -s /bin/false -U tomcat || true")
    run_command(f"sudo chown -R tomcat:tomcat {tomcat_base_installation_path}")
    run_command(f"sudo chown -R root {tomcat_base_installation_path}/conf")
    run_command(f"sudo chmod 750 {tomcat_base_installation_path}/conf")
    run_command(f"sudo find {tomcat_base_installation_path}/conf -type d -exec chmod 750 {{}} \\;")
    run_command(f"sudo find {tomcat_base_installation_path}/conf -type f -exec chmod 440 {{}} \\;")
    run_command(f"sudo chown -R root:tomcat {tomcat_base_installation_path}/lib {tomcat_base_installation_path}/bin")
    with subprocess.Popen(["sudo", "tee", f"{tomcat_service_file_path}"], stdin=subprocess.PIPE, text=True) as f:
        f.communicate(input=tomcat_systemd_file_content)
    run_command("sudo systemctl daemon-reload")
    # run_command("sudo systemctl start tomcat.service")
    run_command("sudo systemctl enable tomcat.service")
    #run_command(f"sudo ufw allow {tomcat_listen_port}")
    run_command(f"sed -iE 's+CLASSPATH=\"$CLASSPATH\"\"$CATALINA_HOME\"/bin/bootstrap.jar+CLASSPATH=\"$CLASSPATH\"\"$CATALINA_HOME\"/bin/bootstrap.jar:$CATALINA_HOME/log4j2/lib/*:$CATALINA_HOME/log4j2/conf:$CATALINA_HOME/conf+' {tomcat_base_installation_path}/bin/catalina.sh")

def install_git():
    run_command("sudo apt update")
    run_command("sudo apt install -y git")

def install_haproxy():
    run_command(f"") #create user haproxy
    run_command(f"curl -L '{haproxy_download_url}' > haproxy")
    run_command("sudo apt install liblua5.3-dev -y")
    run_command("sudo mv haproxy /usr/sbin || echo \"copied already\"")
    run_command(f"sudo useradd -m -d /etc/haproxy -s /bin/false -U haproxy || true")
    run_command("sudo chmod a+x /usr/sbin/haproxy")
    run_command("sudo mkdir /etc/haproxy || echo \"dir exists\"")
    run_command(f"sudo mkdir {haproxy_errors_path} || echo \"dir exists\"")
    run_command(f"sudo chown -R haproxy:haproxy /etc/haproxy || echo \"permissions already given for haproxy\"")
    
    with subprocess.Popen(["sudo", "tee", f"{haproxy_config_file}"], stdin=subprocess.PIPE, text=True) as f:
        f.communicate(input=haproxy_cfg_content)
    run_command(f"sudo chmod a+r {haproxy_config_file}")
    for file_name, content in error_files_content.items():
        with subprocess.Popen(["sudo", "tee", f"{haproxy_errors_path}/{file_name}"], stdin=subprocess.PIPE, text=True) as f:
            f.communicate(input=content)
            

    with subprocess.Popen(["sudo", "tee", f"{haproxy_service_file_path}"], stdin=subprocess.PIPE, text=True) as f:
        f.communicate(input=haproxy_systemd_file_content)
    run_command("sudo systemctl daemon-reload")
    run_command("sudo systemctl enable haproxy.service")
    run_command("sudo systemctl stop haproxy.service")

def install_scylla():
    run_command("sudo apt update")
    run_command("sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys d0a112e067426ab2")
    run_command(f"sudo wget -O /etc/apt/sources.list.d/scylla.list {scylla_list}")
    run_command("sudo apt-get update")
    run_command(f'bash -c "sudo apt-get install -y scylla{{,-server,-jmx,-tools,-tools-core,-kernel-conf,-node-exporter,-conf,-python3}}={scylla_version}"')
    run_command(f"sudo scylla_setup --no-raid-setup --no-coredump-setup --online-discard 1 --nic {nw_if_name} --io-setup 1 --no-version-check")
    run_command("sudo systemctl stop scylla-server")
    run_command("sudo rm -f /usr/bin/java")
    run_command("sudo ln -s /usr/java/jdk-11.0.12/bin/java /usr/bin/java")
    run_command("sudo sed -iE '/After=.*/d; /Before=.*/d; /Requires=.*/d' /lib/systemd/system/scylla-server.service")
    run_command("sudo sed -iE '/Description=/a\Before=tomcat.service haproxy.service' /lib/systemd/system/scylla-server.service")
    run_command("sudo sed -iE '/Before=tomcat.service haproxy.service/a\After=network.target' /lib/systemd/system/scylla-server.service")
    run_command("sudo systemctl daemon-reload")
    run_command("sudo scylla_dev_mode_setup --developer-mode 1")

def install_redpanda():
    run_command(f"curl -1sLf '{redpanda_gpg_key_url}' | gpg --dearmor | sudo tee /usr/share/keyrings/redpanda-redpanda-archive-keyring.gpg >/dev/null")
    with subprocess.Popen(["sudo", "tee", "/etc/apt/sources.list.d/redpanda-redpanda.list"], stdin=subprocess.PIPE) as proc:
        proc.communicate(input=redpanda_repo_content.encode())
    run_command("sudo apt update")
    run_command(f"sudo apt-get install redpanda={redpanda_version}")
    run_command("sudo rpk redpanda mode production")
    run_command("sudo rpk redpanda tune all")
    run_command(f"sudo rpk redpanda config bootstrap --self $(hostname -I)")
    run_command("sudo rpk redpanda config set redpanda.empty_seed_starts_cluster true")
    run_command("sudo systemctl stop redpanda-tuner redpanda || echo 'redpanda tuner, redpanda is in stop state'")
    run_command("sudo systemctl stop redpanda-console || echo 'redpanda console is in stop state'")
    run_command("sudo sed -iE '/After=.*/d; /Before=.*/d; /Requires=.*/d' /lib/systemd/system/redpanda.service")
    run_command("sudo sed -Ei '/Description=/a\Before=tomcat.service haproxy.service' /lib/systemd/system/redpanda.service")
    run_command("sudo sed -Ei '/Before=tomcat.service haproxy.service/a\After=network.target' /lib/systemd/system/redpanda.service")
    run_command("sudo systemctl daemon-reload")


def install_percona():
    run_command("sudo chmod -R 777 /var/cache/debconf")
    run_command(f"sudo echo \"percona-xtradb-cluster-server percona-xtradb-cluster-server/root-pass password {mysql_root_password}\" | debconf-set-selections")
    run_command(f"sudo echo \"percona-xtradb-cluster-server percona-xtradb-cluster-server/re-root-pass password {mysql_root_password}\" | debconf-set-selections")
    run_command(f"sudo echo \"percona-xtradb-cluster-server percona-xtradb-cluster-server/default-auth-override select Use Legacy Authentication Method (Retain MySQL 5.x Compatibility)\" | debconf-set-selections")
    run_command("sudo apt update")
    run_command("sudo apt install curl -y")
    repo_package_url = "https://repo.percona.com/apt/percona-release_latest.generic_all.deb"
    run_command(f"curl -O {repo_package_url}")
    run_command("sudo apt install -y gnupg2 lsb-release")
    run_command("sudo apt install ./percona-release_latest.generic_all.deb")
    run_command("sudo apt update")
    run_command("sudo percona-release setup ps80")
    run_command("sudo percona-release setup pxc80")
    run_command("sudo apt install -y percona-xtradb-cluster")
    run_command("sudo systemctl stop mysql.service || echo 'mysql is in stop state'")
    run_command("sudo sed -iE '/After=.*/d; /Before=.*/d; /Requires=.*/d' /lib/systemd/system/mysql@.service")
    run_command("sudo sed -i '/Description=/a\Before=tomcat.service haproxy.service' /lib/systemd/system/mysql@.service")
    run_command("sudo sed -i '/Before=tomcat.service haproxy.service/a\After=network.target' /lib/systemd/system/mysql@.service")
    run_command("sudo systemctl daemon-reload")
    run_command("sudo chmod -R 600 /var/cache/debconf")
    run_command('bash -c "source ~/.bashrc && exit"')