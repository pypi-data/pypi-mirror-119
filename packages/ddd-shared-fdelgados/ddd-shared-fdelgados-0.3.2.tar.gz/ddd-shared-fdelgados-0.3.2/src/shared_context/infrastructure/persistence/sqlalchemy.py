import abc
from typing import List
from contextlib import contextmanager
from uuid import UUID
from shared_context.domain.model import AggregateRoot, Repository as BaseRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.types import TypeDecorator


@contextmanager
def session_scope(dsn: str):
    session_factory = sessionmaker(bind=create_engine(dsn))

    Session = scoped_session(session_factory)
    session = Session()

    try:
        yield session

        session.commit()
    except Exception:
        session.rollback()

        raise
    finally:
        session.expunge_all()
        session.close()
        Session.remove()


class SessionBuilder:
    _session = None

    @classmethod
    def build(cls, dsn: str):
        if not cls._session:
            db_engine = create_engine(dsn)
            Session = sessionmaker(bind=db_engine)

            cls._session = Session()

        return cls._session


class Repository(BaseRepository):
    def __init__(self, aggregate: AggregateRoot, dsn: str):
        super().__init__(aggregate)

        self._dsn = dsn
        # self.__session = SessionBuilder.build(dsn)

    def add(self, aggregate: AggregateRoot) -> None:
        with session_scope(self._dsn) as session:
            session.add(aggregate)

    def save(self, aggregate: AggregateRoot) -> None:
        with session_scope(self._dsn) as session:
            session.add(aggregate)

    def find(self, **kwargs) -> AggregateRoot:
        with session_scope(self._dsn) as session:
            result = session.query(self.__aggregate).filter_by(**kwargs).first()

            return result

    def find_all(self, **kwargs) -> List[AggregateRoot]:
        with session_scope(self._dsn) as session:
            results = session.query(self.__aggregate).filter_by(**kwargs).all()

            return results


class Orm(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        if subclass is not Orm:
            return NotImplemented

        if hasattr(subclass, "start_mappers") and callable(subclass.start_mappers):
            return True

        return NotImplemented

    @abc.abstractmethod
    def start_mappers(self) -> None:
        raise NotImplemented


class BinaryUUID(TypeDecorator):
    '''Optimize UUID keys. Store as 16 bit binary, retrieve as uuid.
    inspired by:
        http://mysqlserverteam.com/storing-uuid-values-in-mysql-tables/
    '''

    impl = BINARY(16)

    def process_literal_param(self, value, dialect):
        pass

    @property
    def python_type(self):
        pass

    def process_bind_param(self, value, dialect):
        try:
            return value.hex
        except AttributeError:
            try:
                return UUID(value).hex
            except TypeError:
                # for some reason we ended up with the bytestring
                # ¯\_(ツ)_/¯
                # I'm not sure why you would do that,
                # but here you go anyway.
                return value

    def process_result_value(self, value, dialect):
        return UUID(bytes=value)
