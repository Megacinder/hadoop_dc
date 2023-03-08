from typing import List, Optional
import pandas as pd
import logging
from contextlib import closing
from vertica_python import connect
from vertica_python.vertica import connection
from airflow.hooks.dbapi import DbApiHook


def _list_to_sql_list(lst: List):
    if not lst:
        return ''

    if isinstance(lst[0], str):
        return ''.join(f"'{elem}'," for elem in lst)[:-1]
    if isinstance(lst[0], int):
        return ''.join(f"{elem}," for elem in lst)[:-1]
    return ', '.join(lst)


class VerticaHook(DbApiHook):
    """Interact with Vertica."""

    conn_name_attr = 'vertica_conn_id'
    default_conn_name = 'vertica_default'
    conn_type = 'vertica'
    hook_name = 'Vertica'
    supports_autocommit = True

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.schema: Optional[str] = kwargs.pop("schema", None)
        self.conn: connection = None

    def get_conn(self) -> connect:
        """Return verticaql connection object"""
        conn_id = getattr(self, self.conn_name_attr)
        conn = self.get_connection(conn_id)

        conn_config = {
            "host": conn.host or 'localhost',
            "user": conn.login,
            "password": conn.password or '',
            "database": self.schema or conn.schema,
            "prot": int(conn.port) or 5433,
            "log_level": logging.INFO
        }

        self.conn = connect(**conn_config)
        return self.conn

    def bulk_dump(self, table, tmp_file):
        pass

    def bulk_load(self, table, tmp_file):
        pass

    def _get_pandas_df(self, sql, parameters=None, **kwargs):
        with closing(self.get_conn()) as conn:
            with closing(conn.cursor()) as cur:
                cur.register_sql_literal_adapter(list, _list_to_sql_list)
                self.log.info("executing custom get_pandas_df")
                if parameters is not None:
                    cur.execute(sql, parameters)
                else:
                    cur.execute(sql)
                df = pd.DataFrame(cur.fetchall())
                df.columns = [col[0] for col in cur.description]
                return df

    def get_pandas_df(self, sql, parameters=None, **kwargs):
        if isinstance(parameters, list) and any(isinstance(el, list) for el in parameters):
            return self._get_pandas_df(sql, parameters, **kwargs)
        elif isinstance(parameters, dict) and any(isinstance(val, list) for key, val in parameters.items()):
            return self._get_pandas_df(sql, parameters, **kwargs)
        else:
            return super().get_pandas_df(sql, parameters, **kwargs)
