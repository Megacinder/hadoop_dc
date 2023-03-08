from pathlib import Path
from typing import Union, List, Any, Dict

from airflow.models import BaseOperator


class SqlTemplateParser2FileOperator(BaseOperator):
    template_fields = ('sql', 'file', 'sql_params')
    template_fields_renderers = {'sql': 'sql'}
    template_ext = ('.sql',)
    ui_color = '#ededed'

    def __init__(self, *,
                 sql: Union[str, List[str]],
                 file: str,
                 sql_params: dict,
                 **kwargs: Any
                 ) -> None:
        super().__init__(**kwargs)
        self.sql = sql
        self.file = file
        self.sql_params = sql_params

    def pre_execute(self, context: Any):
        self.log.info("pre execute - re-render template fields")
        context["sql_params"] = self.sql_params
        self.render_template_fields(context)

    def execute(self, context: Dict[Any, Any]) -> str:
        self.file = Path(self.file).with_suffix(".sql")
        self.log.info('parsed: {}'.format(self.sql))
        with self.file.open('w', encoding='utf-8') as sql_file:
            sql_file.write(self.sql)

        self.log.info("file: {}".format(str(self.file)))
        return str(self.file)
