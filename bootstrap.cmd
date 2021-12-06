@echo off
SetLocal EnableDelayedExpansion

set SELF=%~dp0
echo "Changing directory to %SELF%."
cd %SELF%

set HADOOP_VERSION=
for /f "tokens=2 delims=:" %%i in ('find /I "HADOOP_VERSION" .env') do set HADOOP_VERSION=%%i
set HADOOP_VERSION=%HADOOP_VERSION: =%

set HIVE_VERSION=
for /f "tokens=2 delims=:" %%i in ('find /I "HIVE_VERSION" .env') do set HIVE_VERSION=%%i
set HIVE_VERSION=%HIVE_VERSION: =%

echo HADOOP_VERSION=%HADOOP_VERSION%
echo HIVE_VERSION=%HIVE_VERSION%

set dirTar=%SELF%tarballs
if not exist "%dirTar%" mkdir "%dirTar%"

set URL=
if not exist "%dirTar%\hadoop-%HADOOP_VERSION%.tar.gz" (
  set URL=https://archive.apache.org/dist/hadoop/common/hadoop-%HADOOP_VERSION%/hadoop-%HADOOP_VERSION%.tar.gz
  echo "Downloading vanilla Hadoop from: !URL!."
  curl -O "!URL!"
  move "hadoop-%HADOOP_VERSION%.tar.gz" tarballs
) else (
    echo "Skipping downloading stage for Hadoop %HADOOP_VERSION%."
)

if not exist "%dirTar%\apache-hive-%HIVE_VERSION%-bin.tar.gz" (
  set URL=https://archive.apache.org/dist/hive/hive-%HIVE_VERSION%/apache-hive-%HIVE_VERSION%-bin.tar.gz
  echo "Downloading vanilla Hive from: !URL!."
  curl -O "!URL!"
  move "apache-hive-%HIVE_VERSION%-bin.tar.gz" tarballs
) else (
   echo "Skipping downloading stage for Hive %HIVE_VERSION%."
)

echo 'Building Dockerfile.'
docker-compose --file docker-compose.yaml --file docker-compose.aux.yaml build

echo 'Done. Use the image with "docker-compose up".'
SetLocal DisableDelayedExpansion
EndLocal
