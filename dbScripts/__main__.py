from scriptFilePaths import *
from runMysql import *
from scriptFilePaths import *
from runCql import *

if __name__ == "__main__":
    # mysql function calls
    createDBandUser(mysqldemo_user)
    runSchemaAndData(mysqlSchema)
    run_qrtz_fles(qrtz_db,qrtz_demo_user,qrtz_schemas)
    # cql function calls
    createKeyspaceAndUser(cql_user_file)
    runSchemaAndData(cql_schema_file)