from vars import *
tomcat_systemd_file_content = f"""
[Unit]
Description=Tomcat 9 servlet container
Before=haproxy.service
After=network.target redpanda.service mysql@bootstrap.service scylla-server.service
Requires=network.target redpanda.service mysql@bootstrap.service scylla-server.service

[Service]
Type=forking
User=tomcat
Group=tomcat
Environment="JAVA_HOME={java_home_path}"
Environment="JAVA_OPTS=-Djava.security.egd=file:///dev/urandom -Djava.awt.headless=true"
Environment="CATALINA_BASE={tomcat_base_installation_path}"
Environment="CATALINA_HOME={tomcat_base_installation_path}"
Environment="CATALINA_PID={tomcat_base_installation_path}/temp/tomcat.pid"
Environment="CATALINA_OPTS=-Xms{min_memory}M -Xmx{max_memory}M -server -XX:+UseParallelGC"
ExecStart={tomcat_base_installation_path}/bin/startup.sh
ExecStop={tomcat_base_installation_path}/bin/shutdown.sh

[Install]
WantedBy=multi-user.target
    """

haproxy_systemd_file_content = f"""
[Unit]
Description=HAProxy Load Balancer
Documentation=man:haproxy(1)
After=network-online.target rsyslog.service redpanda.service mysql@bootstrap.service scylla-server.service tomcat.service
Requires=network-online.target rsyslog.service redpanda.service mysql@bootstrap.service scylla-server.service tomcat.service

[Service]
User=haproxy
Group=haproxy
Environment=\"CONFIG={haproxy_config_file}\" \"PIDFILE=/run/haproxy.pid\" \"EXTRAOPTS=-S /run/haproxy-master.sock\"
ExecStartPre={haproxy_bin_path} -Ws -f $CONFIG -c -q $EXTRAOPTS
ExecStart={haproxy_bin_path} -Ws -f $CONFIG -p $PIDFILE $EXTRAOPTS
ExecReload={haproxy_bin_path} -Ws -f $CONFIG -c -q $EXTRAOPTS
ExecReload=/bin/kill -USR2 $MAINPID
KillMode=mixed
Restart=always
SuccessExitStatus=143
Type=notify

[Install]
WantedBy=multi-user.target
"""