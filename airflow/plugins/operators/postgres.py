from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator


class PostgresAllRowsOperator(PostgresOperator):
    def execute(self, context):
        self.log.info('Executing: %s', self.sql)
        self.hook = PostgresHook(postgres_conn_id=self.postgres_conn_id, schema=self.database)
        result = self.hook.get_records(self.sql, parameters=self.parameters)
        return result
