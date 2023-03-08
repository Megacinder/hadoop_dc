#!/bin/bash

# NOTE: In production (non-Docker) environment it makes sense to do some tuning:
# sysctl -w vm.swappiness=0
# swapoff -a
# swapon -a
# sysctl -w vm.dirty_background_ratio=20
# sysctl -w vm.dirty_ratio=50
# cpufreq-set -r -g performance

echo FORMAT NAMENODE
hdfs namenode -format -force -nonInteractive -clusterID hdc

mkdir -p /tmp/logs/hadoop

echo START HDFS

echo START NAMENODE
echo START NAMENODE
hadoop-daemon.sh start namenode

echo START SECONDARY NAMENODE
hadoop-daemon.sh start secondarynamenode

echo START DATANODE
hadoop-daemon.sh start datanode

echo CREATE HDFS DIRECTORIES
hdfs dfs -mkdir -p /tmp /apps/spark/warehouse /hive/warehouse /user/hadoop
hdfs dfs -chmod -R 1777 /tmp
hdfs dfs -chmod -R 755 /apps

#echo INIT HIVE METASTORE
#PGPASSWORD=postgres psql -v ON_ERROR_STOP=1 --username postgres --host postgres <<-EOSQL
#  DROP DATABASE IF EXISTS hive;
#  CREATE DATABASE hive;
#  GRANT ALL PRIVILEGES ON DATABASE hive TO postgres;
#EOSQL
#schematool -initSchema -dbType postgres

docker run -p 5432:5432 --name postgres-multi
  -e POSTGRES_USERS="postgres:postgres|airflow:airflow"
  -e POSTGRES_DATABASES="postgres:postgres|hive:postgres|airflow:airflow"
  -it --rm lmmdock/postgres-multi

# NOTE: For top-notch availability it makes sense
#   to spin-up a separate container just for Hive.
#   The container should be set up with a HEALTHCHECK and restart policy.
echo START HIVE SERVER
hive --service hiveserver2 --skiphbasecp &

if [ $# -eq 0 ]; then
  tail -f /tmp/hadoop/logs/*
else
  exec "$@"
fi
