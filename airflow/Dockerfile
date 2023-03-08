FROM apache/airflow:2.5.1-python3.8

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        openjdk-11-jdk \
        build-essential \
        libkrb5-dev \
        zip \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    # comment this before first "docker build" and uncomment after (before "docker compose")
#    && apt-get install openssh-client \
#        install openssh-server \
#        systemctl ssh start ssh \
#        systemctl ssh enable


ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME
ENV PYTHONPATH "${PYTHONPATH}:${AIRFLOW_HOME}"

USER airflow

WORKDIR $AIRFLOW_HOME

COPY /airflow/requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir --user -r requirements.txt
