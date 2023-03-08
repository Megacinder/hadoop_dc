from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData(schema="lakehouse")


class BaseModel:

    def todict(self):
        exclude = ('_sa_adapter', '_sa_instance_state')
        return {k: v for k, v in vars(self).items() if not k.startswith('_')
                and not any(hasattr(v, a) for a in exclude)}

    def __repr__(self):
        params = ', '.join(f'{k}={v}' for k, v in self.todict().items())
        return f"{self.__class__.__name__}({params})"


Base = declarative_base(metadata=metadata, cls=BaseModel)
