from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator as SparkSubmit


class SparkSubmitOperator(SparkSubmit):
    template_fields = (
        '_application',
        '_conf',
        '_files',
        '_py_files',
        '_jars',
        '_driver_class_path',
        '_packages',
        '_exclude_packages',
        '_keytab',
        '_principal',
        '_proxy_user',
        '_name',
        '_application_args',
        '_env_vars',
        '_executor_cores',
        '_executor_memory',
        '_driver_memory',
        '_num_executors',
    )
