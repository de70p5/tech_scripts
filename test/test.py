import os


pat=os.getcwd()

file=open(pat+"/inst/Haproxy.cnf","r")

exec(f"cont={file.read()}")