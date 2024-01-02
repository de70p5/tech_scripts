#hostname
hostname="rupid-in-pod1a-node01"
# jdk
jdk_drive_id = "1Vhv1aKynSCoGLDUEhSWCEWS3gjATbFFT"
jdk_file_url = f"https://drive.google.com/uc?export=download&id={jdk_drive_id}&confirm=t"
jdk_version = "11.0.12"
java_installation_path = "/usr/java"
jdk_file_name = f"jdk-{jdk_version}.tar.gz"
java_home_path = f"/usr/java/jdk-{jdk_version}"

#maven
maven_version = "3.8.8"
maven_drive_id = "1kb8ctIxKbwMaIU5SFmQj8zQco_F-Ozan"
maven_file_name = f"apache-maven-{maven_version}-bin.tar.gz"
maven_url = f"https://drive.google.com/uc?export=download&id={maven_drive_id}&confirm=t"
maven_file_download_path = "/tmp"
maven_file_save_path = "/opt"

#tomcat
min_memory="512"
max_memory="1024"
tomcat_version = "9.0.84"
tomcat_drive_id = "1n26prGwVIyk85A8rhMltE5ySP91nNAB_"
tomcat_service_file_path = "/etc/systemd/system/tomcat.service"
tomcat_listen_port = "8080"
tomcat_base_installation_path = "/opt/appxi/prod/tomcat"
tomcat_file_name = f"apache-tomcat-{tomcat_version}.tar.gz"
tomcat_url = f"https://drive.google.com/uc?export=download&id={tomcat_drive_id}&confirm=t"
tomcat_file_download_path = "/tmp"


#haproxy
haproxy_drive_id = "1zzURPKAOA2YO3vrUPBA3uTpVOPCkmFV8"
haproxy_version = "2.8"
haproxy_errors_path = "/etc/haproxy/errors"
haproxy_service_file_path = "/etc/systemd/system/haproxy.service"
haproxy_config_file = "/etc/haproxy/haproxy.cfg"
haproxy_bin_path = "/usr/sbin/haproxy"
haproxy_download_url = f"https://drive.google.com/uc?export=download&id={haproxy_drive_id}&confirm=t"


#scylla
scylla_version="5.0.13-0.20230423.a0ca8abe4-1"
scylla_list = "http://downloads.scylladb.com/deb/debian/scylla-5.0.list"
nw_if_name="ens5"

#redpanda
redpanda_version="22.3.25-1"
redpanda_gpg_key_url = "https://dl.redpanda.com/public/redpanda/gpg.988A7B0A4918BC85.key"
