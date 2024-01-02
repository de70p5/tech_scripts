# scylla imports
from .scylla_server.scyllaVars import *
from .scylla_server.cassCont import *

# redpanda imports
from redpanda.redpandaVars import *
from redpanda.repdandaYamlData import *

#mysql imports
from mysql.mysqlConfContent import *
from mysql.mysqlVars import *

#firewall rules
from firewallRules import *

# import functions
from configure.configureData import scylla_config, mysql_config, redpanda_config, make_dirs, configure_hosts_file, config_firewall_rules

import yaml
import subprocess
import datetime

if __name__=="__main__":
    scylla_config()
    mysql_config()
    redpanda_config()
    make_dirs()
    configure_hosts_file()
    config_firewall_rules()
    