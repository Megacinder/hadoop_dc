JAVA_HOME="$(dirname "$(dirname "$(readlink -f /usr/bin/java)")")"
export JAVA_HOME

export HADOOP_HOME=/opt/hadoop

export HADOOP_IDENT_STRING="hadoop"

export HADOOP_LOG_DIR=/tmp/hadoop/logs

export HADOOP_OS_TYPE=${HADOOP_OS_TYPE:-$(uname -s)}

if [ -z "${HADOOP_HEAPSIZE}" ]; then
  export HADOOP_HEAPSIZE=512
fi
