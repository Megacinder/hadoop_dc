import uuid

import pandas as pd
from typing import Any

from airflow.models.xcom import BaseXCom


class LocalFileSysXCom(BaseXCom):
    PREFIX = '/tmp/data_'

    @staticmethod
    def serialize_value(value: Any):
        if isinstance(value, pd.DataFrame):
            object_name = LocalFileSysXCom.PREFIX + str(uuid.uuid4())
            value.to_csv(object_name, index=False, sep=";", quotechar='"')
            value = object_name
        return BaseXCom.serialize_value(value)

    @staticmethod
    def deserialize_value(result) -> Any:
        result = BaseXCom.deserialize_value(result)
        if isinstance(result, str) and result.startswith(LocalFileSysXCom.PREFIX):
            object_name = result
            result = pd.read_csv(object_name, header=0, sep=";", quotechar='"')
        return result
