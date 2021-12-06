#!/usr/bin/env bash

set -e

SELF="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Changing directory to ${SELF}."
cd "${SELF}"

source .env

mkdir -p "${SELF}/tarballs/"
if [ ! -e "${SELF}/tarballs/hadoop-${HADOOP_VERSION}.tar.gz" ]; then
  URL="https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz"
  echo "Downloading vanilla Hadoop from: ${URL}."
  curl -O "${URL}"
  mv "hadoop-${HADOOP_VERSION}.tar.gz" tarballs
else
  echo "Skipping downloading stage for Hadoop ${HADOOP_VERSION}."
fi
if [ ! -e "${SELF}/tarballs/apache-hive-${HIVE_VERSION}-bin.tar.gz" ]; then
  URL="https://archive.apache.org/dist/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz"
  echo "Downloading vanilla Hive from: ${URL}."
  curl -O "${URL}"
  mv "apache-hive-${HIVE_VERSION}-bin.tar.gz" tarballs
else
  echo "Skipping downloading stage for Hive ${HIVE_VERSION}."
fi

echo 'Cleanup'
docker-compose --file docker-compose.yaml --file docker-compose.aux.yaml down || true
docker volume rm hadoop hive spark airflow || true

echo 'Building Dockerfile.'
docker-compose --file docker-compose.yaml --file docker-compose.aux.yaml build

echo 'Done. Use the image with "docker-compose up".'
