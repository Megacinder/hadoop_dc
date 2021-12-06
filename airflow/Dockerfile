FROM python:3.8
FROM redhat/ubi8

ARG AIRFLOW_VERSION

ENV AIRFLOW_HOME=/opt/airflow

WORKDIR ${AIRFLOW_HOME}

USER root

RUN set -xe \
    && yum update -y \
    && yum install -y python3-pip

RUN \
    yum update -y \
    && yum install -y \
        https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm \
        gcc \
        make \
    && yum install -y postgresql13 \
    && pip3 install -U pip \
    && pip install --no-cache-dir pypandoc \
    && pip3 install pandas pyspark==2.4.8 openpyxl pyyaml requests \
    && pip3 install --use-deprecated legacy-resolver apache-airflow[crypto,postgres]==${AIRFLOW_VERSION}  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-3.6.txt" \
    && chown hadoop:hadoop -R /opt/airflow \
    && yum clean all \
    && rm -rf /tmp/* /var/tmp/* /root/.cache/*

USER hadoop

COPY --chown=hadoop:hadoop airflow/entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]
