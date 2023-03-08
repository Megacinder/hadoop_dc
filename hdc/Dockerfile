FROM redhat/ubi9

ARG HADOOP_VERSION
ARG HIVE_VERSION

ADD tarballs/hadoop-${HADOOP_VERSION}.tar.gz /opt
ADD tarballs/apache-hive-${HIVE_VERSION}-bin.tar.gz /opt

RUN echo 'INSTALL' \
    && yum update -y \
    && yum install -y \
        procps \
        java-1.8.0-openjdk \
        https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm \
    && yum install -y postgresql15 \
    && echo 'CREATE USER' \
    && useradd --system --create-home --user-group --shell /bin/bash hadoop \
    && echo 'HADOOP' \
    && mv /opt/hadoop-${HADOOP_VERSION} /opt/hadoop \
    && mv /opt/apache-hive-${HIVE_VERSION}-bin /opt/hive \
    && rm /opt/hive/lib/log4j-slf4j* \
    && mkdir -p /opt/hadoop-runtime \
    && chown hadoop:hadoop -R /opt \
    && echo 'CLEANUP' \
    && yum clean all \
    && rm -rf /tmp/* /var/tmp/*

USER hadoop

ENV \
    TZ=UTC \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    JAVA_HOME=/usr/lib/jvm/jre-1.8.0-openjdk \
    HADOOP_HOME=/opt/hadoop \
    HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop \
    HIVE_HOME=/opt/hive \
    HIVE_CONF_DIR=/opt/hive/conf \
    SPARK_CONF_DIR=/opt/spark/conf \
    PATH=${PATH}:/opt/hadoop/bin:/opt/hadoop/sbin:/opt/hive/bin

COPY --chown=hadoop:hadoop \
    confs/hadoop-env.sh \
    confs/log4j.properties \
    confs/core-site.xml \
    confs/hdfs-site.xml \
    confs/mapred-site.xml \
    ${HADOOP_CONF_DIR}/

COPY --chown=hadoop:hadoop \
    confs/hive-site.xml \
    confs/hive-env.sh \
    ${HIVE_CONF_DIR}/

COPY --chown=hadoop:hadoop \
    confs/spark-defaults.conf \
    confs/spark-env.sh \
    confs/spark-log4j.properties \
    ${SPARK_CONF_DIR}/

COPY --chown=hadoop:hadoop hdc/entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]

WORKDIR /opt

RUN chmod 755 /entrypoint.sh \
    && mv ${SPARK_CONF_DIR}/{spark-,}log4j.properties
