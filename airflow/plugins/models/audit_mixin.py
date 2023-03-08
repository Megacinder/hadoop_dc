from datetime import datetime

from sqlalchemy import Column, DateTime, func


class AuditMixin(object):
    created_at = Column(DateTime(timezone=False), default=datetime.now(), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), default=datetime.now(), server_default=func.now(),
                        onupdate=func.now())
