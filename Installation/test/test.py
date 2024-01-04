import os
import sys

basePath=os.getcwd()
# fileArguments=sys.argv[1:]
# installConfFile, haproxyErrorsFile, haproxyConfFile, haproxyServiceFile, tomcatServiceFile = [basePath+i for i in fileArguments]
installConfFile=open(basePath+"/InstallConf/Install.cnf")
vars=list(installConfFile.readlines())
for i in vars:
    exec(f"{i.split('=')[0].strip()} = \"{i.split('=')[1].strip()}\"")
    print(i)
tomcatServiceFile=open(basePath+"/Tomcat.service")

file=open(tomcatServiceFile,"r")
fileData=file.read()
exec(f"tomcatServiceFileContent={fileData}")
print(tomcatServiceFileContent)
file.close()