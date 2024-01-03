import subprocess
from dbCredentials import *
from scriptFilePaths import *


def run_command(command,timer=None):
    return subprocess.run(command,shell=True)

def createKeyspaceAndUser(demo_user):
    run_command(f"/usr/bin/cqlsh -u {scyllaUser} -p {scyllaPassword} {scyllaHostIp} {cqlport} -f {cql_user_file}")

def runSchemaAndData(schemapath):
    run_command(f"/usr/bin/cqlsh -k {scyllaDb} -u {scyllaUser} -p {scyllaPassword} {scyllaHostIp} {cqlport} -f {cql_schema_file}")
