import subprocess
from dbCredentials import *

def run_command(command,timer=None):
    return subprocess.run(command,shell=True)

def createDBandUser(demo_user):
    run_command(f"/usr/bin/mysql  -u {mysqlUser} -p{mysqlPassword} < {demo_user}")

def runSchemaAndData(schemapath, basedatapath):
    run_command(f"/usr/bin/mysql  -u {mysqlUser} -p{mysqlPassword} {mysqlDb}< {schemapath}")
    run_command(f"/usr/bin/mysql  -u {mysqlUser} -p{mysqlPassword} {mysqlDb}< {basedatapath}")


def run_qrtz_fles(qrtz_db,qrtz_demo_user,qrtz_schemas):
    run_command(f"/usr/bin/mysql  -u {mysqlUser} -p{mysqlPassword} < {qrtz_demo_user}")
    run_command(f"/usr/bin/mysql  -u {mysqlUser} -p{mysqlPassword} {qrtz_db} < {qrtz_schemas}")