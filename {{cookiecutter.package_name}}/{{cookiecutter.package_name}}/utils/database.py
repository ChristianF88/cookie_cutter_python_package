#!/usr/bin/env python
"""
-------------------------------------------------------
2021-02-01 -- Christian Foerster
christian.foerster@eawag.ch
-------------------------------------------------------
"""
from sqlalchemy import create_engine
from sqlalchemy import Table, String, DateTime, Column, Integer, Float, ForeignKey
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from collections.abc import Iterable


class AlchemySession:
    def __init__(self, engine):
        self.__engine = engine

    def __enter__(self):
        session = sessionmaker(bind=self.__engine)
        self.session = session()
        return self.session

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.session.close()


def database_schema(db_engine):
    base = declarative_base()

    class MeteoStation(base):
        __tablename__ = 'meteo_station'
        idx = Column(Integer, primary_key=True)
        ts = Column(DateTime, index=True)
        a = Column(Float)
        b = Column(Integer)
        c = Column(String)

    class RainStation(base):
        __tablename__ = 'rain_station'
        idx = Column(Integer, primary_key=True)
        ts = Column(DateTime, index=True)
        a = Column(Float)
        b = Column(Integer)
        c = Column(String)

    base.metadata.create_all(db_engine)

    return MeteoStation, RainStation


class Database:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    DB_ENGINE = {
        'sqlite': 'sqlite:///{database}',
        'postgresql': 'postgresql+psycopg2://{user}:{password}@{host}/{database}',
        'mysql': 'mysql://{user}:{password}@{host}/{database}'
    }

    # Main DB Connection Ref Obj
    db_engine = None

    def __init__(self, dbtype, user=None, password=None, database=None, host=None):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(**locals())
            self.db_engine = create_engine(engine_url)

        else:
            print(f"DBType '{dbtype}' is not found in DB_ENGINE")

    def is_empty(self, table):
        return self.dump_table(table) == []

    @staticmethod
    def __format_return(tables):
        if isinstance(tables, Iterable):
            return {table.__tablename__: table for table in tables}
        else:
            return {tables.__tablename__: tables}

    @staticmethod
    def convert(row):
        if row:
            dic = row.__dict__.copy()
            del dic['_sa_instance_state']
            return dic
        else:
            return row

    def init_database_model(self, schema):
        """
        Examples of table definition
        ----------------------------

        https://www.pythonsheets.com/notes/python-sqlalchemy.html
        https://leportella.com/sqlalchemy-tutorial.html
        https://docs.sqlalchemy.org/en/13/core/type_basics.html?highlight=types#module-sqlalchemy.types

        """

        tables = schema(self.db_engine)

        return Database.__format_return(tables)

    def fill_table(self, table, rows):
        """
        rows: list containing dict (key colname: val value)
        """
        with AlchemySession(self.db_engine) as session:
            for entry in rows:
                session.add(table(**entry))
            session.commit()

    def iter_table(self, table):
        with AlchemySession(self.db_engine) as session:
            tbl = session.query(table)
            for row in tbl:
                yield Database.convert(row)

    def dump_table(self, table):
        with AlchemySession(self.db_engine) as session:
            return session.query(table).all()

    def execute_query(self, query, commit=False):
        with AlchemySession(self.db_engine) as session:
            session.execute(query)

            if commit:
                session.commit()

    def read_last_row(self, table):
        """Assumes timestamp is a column after which will be ordered"""
        with AlchemySession(self.db_engine) as session:
            row = session.query(table).order_by(table.timestamp.desc()).limit(1).all()

        if row:
            row = row[0]

        return Database.convert(row)


class SQLite3(Database):
    def __init__(self, **connection_details):
        super().__init__("sqlite", **connection_details)


class MySQL(Database):
    def __init__(self, **connection_details):
        super().__init__("mysql", **connection_details)


class PostgreSQL(Database):
    def __init__(self, **connection_details):
        super().__init__("postgresql", **connection_details)
