import subprocess
import os
import sys
import datetime

def set_hostname():
    run_command(f"sudo hostnamectl set-hostname {hostname}")

def run_command(command):
    print(f"Running command: {command}")
    subprocess.run(command, shell=True, check=True)

def install_java():
    run_command(f"curl -L 'https://drive.google.com/uc?export=download&id={jdkDriveId}&confirm=t' > {jdkFileName}")
    run_command(f"sudo mkdir -p {javaInstallationPath}")
    run_command(f"sudo tar -xzvf {jdkFileName} -C /usr/java")
    run_command(f'echo \'export PATH=$PATH:{javaHomePath}/bin\' >> ~/.bashrc')
    run_command(f'echo \'export JAVA_HOME={javaHomePath}\' >> ~/.bashrc')
    #run_command(f"sudo ln -s /usr/java/jdk-{jdk_version}/bin/java /usr/bin/java")
    
def install_maven():
    run_command(f"curl -L 'https://drive.google.com/uc?export=download&id={mavenDriveId}&confirm=t' > {mavenFileName}")
    run_command(f"sudo tar -xvzf {mavenFileName} -C /opt")
    run_command(f"echo \'export PATH=$PATH:{mavenFileSavePath}/apache-maven-{mavenVersion}/bin\' >> ~/.bashrc")
    run_command(f"echo \'export M2_HOME={mavenFileSavePath}/apache-maven-{mavenVersion}\' >> ~/.bashrc")
    run_command(f"echo \'export M2={mavenFileSavePath}/apache-maven-{mavenVersion}/bin\' >> ~/.bashrc")
    
def install_tomcat():
    run_command(f"curl -L 'https://drive.google.com/uc?export=download&id={tomcatDriveId}&confirm=t' > {tomcatFileName}")
    run_command(f"sudo mkdir -p {tomcatBaseInstallationPath} || echo \"Tomcat dir is created\"")
    run_command(f"sudo tar -xvzf {tomcatFileName} -C {tomcatBaseInstallationPath}")
    run_command(f"sudo cp -rdp {tomcatBaseInstallationPath}/apache-tomcat-9.0.84/* {tomcatBaseInstallationPath}")
    run_command(f"sudo rm -rf {tomcatBaseInstallationPath}/apache-tomcat-9.0.84")
    run_command(f"sudo useradd -m -d {tomcatBaseInstallationPath} -s /bin/false -U tomcat || true")
    run_command(f"sudo chown -R tomcat:tomcat {tomcatBaseInstallationPath}")
    run_command(f"sudo chown -R root {tomcatBaseInstallationPath}/conf")
    run_command(f"sudo chmod 750 {tomcatBaseInstallationPath}/conf")
    run_command(f"sudo find {tomcatBaseInstallationPath}/conf -type d -exec chmod 750 {{}} \\;")
    run_command(f"sudo find {tomcatBaseInstallationPath}/conf -type f -exec chmod 440 {{}} \\;")
    run_command(f"sudo chown -R root:tomcat {tomcatBaseInstallationPath}/lib {tomcatBaseInstallationPath}/bin")
    with subprocess.Popen(["sudo", "tee", f"{tomcatServiceFilePath}"], stdin=subprocess.PIPE, text=True) as f:
        f.communicate(input=tomcatServiceFileContent)
    run_command("sudo systemctl daemon-reload")
    # run_command("sudo systemctl start tomcat.service")
    run_command("sudo systemctl enable tomcat.service")
    #run_command(f"sudo ufw allow {tomcat_listen_port}")
    run_command(f"sed -iE 's+CLASSPATH=\"$CLASSPATH\"\"$CATALINA_HOME\"/bin/bootstrap.jar+CLASSPATH=\"$CLASSPATH\"\"$CATALINA_HOME\"/bin/bootstrap.jar:$CATALINA_HOME/log4j2/lib/*:$CATALINA_HOME/log4j2/conf:$CATALINA_HOME/conf+' {tomcatBaseInstallationPath}/bin/catalina.sh")

def install_git():
    run_command("sudo apt update")
    run_command("sudo apt install -y git")

def install_haproxy():
    run_command(f"curl -L 'https://drive.google.com/uc?export=download&id={haproxyDriveId}&confirm=t' > haproxy")
    run_command("sudo apt install liblua5.3-dev -y")
    run_command("sudo mv haproxy /usr/sbin || echo \"copied already\"")
    run_command(f"sudo useradd -m -d /etc/haproxy -s /bin/false -U haproxy || true")
    run_command("sudo chmod a+x /usr/sbin/haproxy")
    run_command("sudo mkdir /etc/haproxy || echo \"dir exists\"")
    run_command(f"sudo mkdir {haproxyErrorsPath} || echo \"dir exists\"")
    run_command(f"sudo chown -R haproxy:haproxy /etc/haproxy || echo \"permissions already given for haproxy\"")
    
    with subprocess.Popen(["sudo", "tee", f"{haproxyConfigFile}"], stdin=subprocess.PIPE, text=True) as f:
        f.communicate(input=haproxyConfContent)
    run_command(f"sudo chmod a+r {haproxyConfigFile}")
    for file_name, content in errorFilesContent.items():
        with subprocess.Popen(["sudo", "tee", f"{haproxyErrorsPath}/{file_name}"], stdin=subprocess.PIPE, text=True) as f:
            f.communicate(input=content)
            

    with subprocess.Popen(["sudo", "tee", f"{haproxyServiceFilePath}"], stdin=subprocess.PIPE, text=True) as f:
        f.communicate(input=haproxyServiceFileContent)
    run_command("sudo systemctl daemon-reload")
    run_command("sudo systemctl enable haproxy.service")
    run_command("sudo systemctl stop haproxy.service")

def install_scylla():
    run_command("sudo apt update")
    run_command("sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys d0a112e067426ab2")
    run_command(f"sudo wget -O /etc/apt/sources.list.d/scylla.list {scyllaList}")
    run_command("sudo apt-get update")
    run_command(f'bash -c "sudo apt-get install -y scylla{{,-server,-jmx,-tools,-tools-core,-kernel-conf,-node-exporter,-conf,-python3}}={scyllaVersion}"')
    run_command(f"sudo scylla_setup --no-raid-setup --no-coredump-setup --online-discard 1 --nic {nwIfName} --io-setup 1 --no-version-check")
    run_command("sudo systemctl stop scylla-server")
    run_command("sudo rm -f /usr/bin/java")
    run_command("sudo ln -s /usr/java/jdk-11.0.12/bin/java /usr/bin/java")
    run_command("sudo sed -iE '/After=.*/d; /Before=.*/d; /Requires=.*/d' /lib/systemd/system/scylla-server.service")
    run_command("sudo sed -iE '/Description=/a\Before=tomcat.service haproxy.service' /lib/systemd/system/scylla-server.service")
    run_command("sudo sed -iE '/Before=tomcat.service haproxy.service/a\After=network.target' /lib/systemd/system/scylla-server.service")
    run_command("sudo systemctl daemon-reload")
    run_command("sudo scylla_dev_mode_setup --developer-mode 1")

def install_redpanda():
    run_command(f"curl -1sLf '{redpandaGpgKeyUrl}' | gpg --dearmor | sudo tee /usr/share/keyrings/redpanda-redpanda-archive-keyring.gpg >/dev/null")
    redpandaRepoContent = """# Source: Redpanda
    # Site: https://github.com/redpanda-data/redpanda/
    # Repository: Redpanda / redpanda
    # Description: Redpanda is a streaming data platform for developers. Kafka API compatible. 10x faster. No ZooKeeper. No JVM!

    deb [signed-by=/usr/share/keyrings/redpanda-redpanda-archive-keyring.gpg] https://dl.redpanda.com/public/redpanda/deb/ubuntu jammy main

    deb-src [signed-by=/usr/share/keyrings/redpanda-redpanda-archive-keyring.gpg] https://dl.redpanda.com/public/redpanda/deb/ubuntu jammy main
    """
    with subprocess.Popen(["sudo", "tee", "/etc/apt/sources.list.d/redpanda-redpanda.list"], stdin=subprocess.PIPE) as proc:
        proc.communicate(input=redpandaRepoContent.encode())
    run_command("sudo apt update")
    run_command(f"sudo apt-get install redpanda={redpandaVersion}")
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
    run_command(f"sudo echo \"percona-xtradb-cluster-server percona-xtradb-cluster-server/root-pass password {mysqlRootPassword}\" | debconf-set-selections")
    run_command(f"sudo echo \"percona-xtradb-cluster-server percona-xtradb-cluster-server/re-root-pass password {mysqlRootPassword}\" | debconf-set-selections")
    run_command(f"sudo echo \"percona-xtradb-cluster-server percona-xtradb-cluster-server/default-auth-override select Use Legacy Authentication Method (Retain MySQL 5.x Compatibility)\" | debconf-set-selections")
    run_command("sudo apt update")
    run_command("sudo apt install curl -y")
    run_command(f"curl -O {perconaRepoPackageUrl}")
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

start_time = datetime.now()

basePath=os.getcwd()
fileArguments=sys.argv[1:]
installConfFile, haproxyErrorDict, haproxyConfFile, haproxyServiceFile, tomcatServiceFile = [basePath+i for i in fileArguments]
for i in installConfFile.readlines():
    exec(f"{i.split('=')[0]} = \"{i.split('=')[1].strip()}\"")

file=open(haproxyErrorsFile,"r")
exec(f"errorFilesContent={file.read()}")
file.close()

file=open(haproxyConfFile,"r")
fileData=file.read()
haproxyConfContent=f"""{fileData}"""
file.close()

file=open(haproxyServiceFile,"r")
fileData=file.read()
exec(f"haproxyServiceFileContent={fileData}")
file.close()

file=open(tomcatServiceFile,"r")
fileData=file.read()
exec(f"tomcatServiceFileContent={fileData}")
file.close()

run_command("sudo apt install curl -y")
set_hostname()
install_java()
install_maven()
install_tomcat()
install_git()
install_haproxy()
install_scylla()
install_redpanda()
install_percona()
end_time=datetime.now()
print("Time elapsed is: ",end_time-start_time)