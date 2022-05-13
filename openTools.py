import os

print("start hadoop ... ")
os.system("../start-hadoop.sh")

print("start hbase ... ")
os.system("start-hbase.sh")

print("start kafka ... ")
os.system("../start-kafka-zookeeper.sh")
