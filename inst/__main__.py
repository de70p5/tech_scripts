import subprocess
from datetime import datetime
from instFunc import *

start_time = datetime.now()

if __name__ == "__main__":
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