# HDC -- Hadoop Development [Pseudo-Distributed] Cluster.

HDC -- это псевдо-распределенный кластер Hadoop для
**локальной разработки и тестирования**.

Псевдо-распределенный -- значит кластер из одной ноды.
Репликация отключена (dfs.replication = 1) и размер блока
по-умолчанию (dfs.blocksize) установлен в 32 Мб.

В настоящий момент поднимается HDFS, без YARN.
MapReduce работает в локальном режиме.

Также поднимается Hive с движком MapReduce и метастором в Postgres.


## Setup and Build

Для загрузки исходников и сборки нужно, чтобы были доступны эти домены:
- nexus-ci.corp.dev.vtb
- bitbucket.region.vtb.ru

Также нужно сделать Always Trust для их сертификатов.

Далее, для доступа с локальной машины в Web UI и не только,
**один раз** нужно сделать предварительную настройку
**/etc/hosts** (на Linux и MacOS), или **Windows\System32\Drivers\etc\hosts**.
Заменить:
```text
127.0.0.1   localhost
```

На:
```text
127.0.0.1   localhost hdc
```

Далее, **один раз** склонировать проект. На Linux/MacOS:
```shell
git clone https://bitbucket.region.vtb.ru/scm/drp/hadoop_dev_cluster.git
```

Далее вся работа происходит в пределах склонированного проекта:
```shell
cd hadoop_dev_cluster
```


### Automated Build

На Linux/MacOS можно воспользоваться скриптом сборки:
```shell
./bootstrap.sh
```


### Manual Build

Для сборки руками, перед сборкой нужно скачать tar.gz архив Hadoop той версии,
которая прописана в файле `docker-compose.yaml`,
и положить ее в директорию `tarballs`.
Архивы можно найти тут: https://archive.apache.org/dist/hadoop/common/.

Например (для Hadoop 2.7.7 и Hive 2.3.8):
```shell
curl -O https://archive.apache.org/dist/hadoop/common/hadoop-2.7.7/hadoop-2.7.7.tar.gz
mkdir -p tarballs
mv hadoop-2.7.7.tar.gz tarballs

curl -O https://archive.apache.org/dist/hive/hive-2.3.8/apache-hive-2.3.8-bin.tar.gz
mv apache-hive-2.3.8-bin.tar.gz tarballs
```

Чтобы собрать образ:
```shell
docker-compose --file docker-compose.yaml --file docker-compose.aux.yaml build
```

Иногда имеет смысл удалить старый мусор (прежде всего тома):
```shell
docker-compose --file docker-compose.yaml --file docker-compose.aux.yaml down || true
docker volume rm hadoop hive spark || true
```

## Run and Stop

Для запуска только Hadoop:
```shell
docker-compose up
```

Для запуска Hadoop и всего остального (Airflow):
```shell
docker-compose --file docker-compose.yaml --file docker-compose.aux.yaml up
```

Для остановки:
```shell
docker-compose down
```


## Use

### HDFS Web UI

Web UI будет доступен тут: http://localhost:50070.

### PySpark Example

Для подключения через Spark (**пример недоделан**), достаточно указать RPC
адрес NameNode -- `hdfs://localhost:8020`:
```python
from pyspark import SparkConf, sql

conf = SparkConf().setAll([
    ('spark.app.name', __name__),
    ('spark.master', 'local[1]'),
])
with sql.SparkSession.builder.config(conf=conf).getOrCreate() as spark:
    df = spark.range(500).toDF('number')

    # Адрес NameNode:
    filename = 'hdfs://localhost:8020/my_file.parquet'

    df.write.mode('overwrite').save(path=filename, format='parquet')
```

### CLI Access

Самый простой способ это использовать **docker container exec**:
```shell
docker container exec -it hadoop_dev_cluster_hadoop_1 bash
```

С этого момента доступен HDFS:
```shell
hdfs dfs -ls /
```

И Hive:
```shell
beeline -u jdbc:hive2://localhost:10000 hadoop 123
```

Другой вариант, это скопировать инсталляцию Hadoop, включая конфиги, из
Docker в локальную файловую систему:
```shell
mkdir -p ./hadoop
docker cp hadoop_dev_cluster_hadoop_1:/opt/hadoop ./hadoop 
docker cp hadoop_dev_cluster_hadoop_1:/opt/hive ./hadoop

sed -i -E 's/export JAVA_HOME.*//g' ./hadoop/hadoop/etc/hadoop/hadoop-env.sh

export HADOOP_HOME=./hadoop/hadoop
export HIVE_HOME=./hadoop/hive
export PATH=${HADOOP_HOME}/bin:${HIVE_HOME}/bin:${PATH}
```

С этого момента мы можем обращаться в HDFS с локальной машины:
```shell
hdfs dfs -ls /
```

И в Hive:
```shell
beeline -u jdbc:hive2://localhost:10000 hadoop 123
```

### User Configuration

Кастомное конфигурирование делается через **docker-compose.override.yaml**:
```yaml
version: "3.8"

services:
  hadoop:
    volumes:
      - ./hdfs-site.xml:/opt/hadoop/etc/hadoop/hdfs-site.xml
```

Далее при старте `docker-compose up` у нас подхватится кастомный конфиг.

TODO: Пушить тэгированный образ в Nexus.
