from typing import Any, Dict, List, Mapping, Iterable, Union, Optional

from airflow.models import BaseOperator
from pandas import DataFrame

from hooks.vertica import VerticaHook


class Vertica2DataFrameOperator(BaseOperator):
    template_fields = ('parameters', 'sql',)
    template_fields_renderers = {'sql': 'sql'}
    template_ext = ('.sql',)
    ui_color = '#ededed'

    def __init__(self, *,
                 sql: Union[str, List[str]],
                 vertica_conn_id: str = 'vertica_default',
                 parameters: Optional[Union[Mapping, Iterable]] = None,
                 **kwargs: Any
                 ) -> None:
        super().__init__(**kwargs)
        self.sql = sql
        self.vertica_conn_id = vertica_conn_id
        self.parameters = parameters
        self.hook = None

    def execute(self, context: Dict[Any, Any]) -> DataFrame:
        self.log.info('Executing: %s', self.sql)
        self.hook = VerticaHook(vertica_conn_id=self.vertica_conn_id)
        pandas_df = self.hook.get_pandas_df(sql=self.sql, parameters=self.parameters)

        return pandas_df
