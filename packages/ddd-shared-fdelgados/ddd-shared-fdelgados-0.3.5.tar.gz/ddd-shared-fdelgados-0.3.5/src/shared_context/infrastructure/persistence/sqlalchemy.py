import abc
import threading
from typing import List
from contextlib import contextmanager
from uuid import UUID
from shared_context.domain.model import AggregateRoot, Repository as BaseRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.types import TypeDecorator


class SessionBuilder:
    _session = None
    _lock = threading.Lock()

    @classmethod
    def build(cls, dsn: str):
        if not cls._session:
            with cls._lock:
                if not cls._session:
                    session_factory = sessionmaker(bind=create_engine(dsn), expire_on_commit=False)
                    cls._session = scoped_session(session_factory)
        return cls._session


@contextmanager
def session_scope(dsn: str):
    Session = SessionBuilder.build(dsn)
    session = Session()

    try:
        yield session
    except Exception:
        raise
    finally:
        session.close()
        Session.remove()


class Repository(BaseRepository):
    def __init__(self, aggregate: AggregateRoot, dsn: str):
        self._aggregate = aggregate
        self._dsn = dsn

    def create_connection(self):
        return create_engine(self._dsn)

    def add(self, aggregate: AggregateRoot) -> None:
        with session_scope(self._dsn) as session:
            session.add(aggregate)
            session.commit()

    def save(self, aggregate: AggregateRoot) -> None:
        with session_scope(self._dsn) as session:
            session.add(aggregate)
            session.commit()

    def find(self, **kwargs) -> AggregateRoot:
        with session_scope(self._dsn) as session:
            result = session.query(self._aggregate).filter_by(**kwargs).first()

        return result

    def find_all(self, **kwargs) -> List[AggregateRoot]:
        with session_scope(self._dsn) as session:
            results = session.query(self._aggregate).filter_by(**kwargs).all()

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
