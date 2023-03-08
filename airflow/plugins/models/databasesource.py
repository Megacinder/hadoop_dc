import enum
import logging
from dataclasses import dataclass
from typing import Optional
from datetime import date

from airflow.utils.log.logging_mixin import LoggingMixin
from sqlalchemy import Column, Integer, String, JSON, Date
from sqlalchemy.dialects.postgresql import ENUM

from plugins.models.base import Base
from plugins.models.audit_mixin import AuditMixin

log = logging.getLogger(__name__)


class Load(enum.Enum):
    Y = 'Y'
    N = 'N'

    def __str__(self):
        return self.name

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

    @classmethod
    def coerce(cls, item):
        item = cls(item) if not isinstance(item, cls) else item
        return item.value


class LoadType(enum.Enum):
    FULL = 'FULL'
    INCREMENTAL = 'INCREMENTAL'

    def __str__(self):
        return self.name

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

    @classmethod
    def coerce(cls, item):
        item = cls(item) if not isinstance(item, cls) else item
        return item.value


@dataclass
class DatabaseSource(Base, LoggingMixin, AuditMixin):
    __tablename__ = 'database_source'
    __table_args__ = {
        'extend_existing': True,
    }

    id = Column(Integer(), primary_key=True)
    table_name = Column(String(500), nullable=False)
    schema = Column(String(500), nullable=False)
    load = Column(ENUM(Load), default=Load.Y.value, server_default=Load.Y.value, nullable=False)
    load_type = Column(ENUM(LoadType), nullable=False)
    last_load_type = Column(ENUM(LoadType), nullable=False)
    next_load_type = Column(ENUM(LoadType), nullable=False)
    spark_submit = Column(JSON(), nullable=False)
    target_options = Column(JSON(), nullable=False)
    jdbc_options = Column(JSON(), nullable=True)
    sql_script = Column(String(500), nullable=True)
    incremental_load_date = Column(Date(), nullable=True)
    last_load_date = Column(Date(), nullable=True)

    def __init__(
            self,
            table_name: Optional[str] = None,
            schema: Optional[str] = None,
            load: Optional[str] = None,
            load_type: Optional[str] = None,
            last_load_type: Optional[str] = None,
            next_load_type: Optional[str] = None,
            spark_submit: Optional[dict] = None,
            target_options: Optional[dict] = None,
            jdbc_options: Optional[dict] = None,
            sql_script: Optional[str] = None,
            incremental_load_date: Optional[date] = None,
            last_load_date: Optional[date] = None):
        super().__init__()
        self.table_name = table_name
        self.schema = schema
        self.load = load
        self.load_type = load_type
        self.last_load_type = last_load_type
        self.next_load_type = next_load_type
        self.spark_submit = spark_submit
        self.target_options = target_options
        self.db_options = jdbc_options
        self.sql_script = sql_script
        self.incremental_load_date = incremental_load_date
        self.last_load_date = last_load_date

    def get_conf(self):
        conf = {
            "database": self.schema,
            "load_type": self.next_load_type.name,
            "table": self.table_name,
            "load_date": self.incremental_load_date.isoformat() if self.incremental_load_date else None
        }

        conf["spark_submit"] = self.spark_submit.get(conf["load_type"], "FULL")
        conf["target"] = self.target_options.get(conf["load_type"], "FULL")

        if self.jdbc_options:
            conf["jdbc"] = self.jdbc_options.get(conf["load_type"], "FULL")
        if self.sql_script:
            conf["table"] = self.sql_script

        return conf
