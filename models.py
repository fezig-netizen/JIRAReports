from sqlalchemy import MetaData, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

meta = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
      })

Base = declarative_base(metadata=meta)

class Epic(Base):
    __tablename__ = 'epics'
    Id = Column(Integer, primary_key=True)
    Date = Column(Date)
    Key = Column(String)
    Summary = Column(String)
    Status = Column(String)
    Issues = relationship('Issue')

class Issue(Base):
    __tablename__ = 'issues'
    Id = Column(Integer, primary_key=True)
    Date = Column(Date)
    Key = Column(String)
    Summary = Column(String)
    IssueType = Column(String)
    Status = Column(String)
    Estimate = Column(Integer)
    EpicId = Column(Integer, ForeignKey('epics.Id'))

class FixVersion(Base):
    __tablename__ = 'fixversions'
    Id = Column(Integer, primary_key=True)
    Date = Column(Date)
    Name = Column(String)
    JiraId = Column(Integer)
