from sqlalchemy import MetaData, Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# The naming convention has to be here to support automatic naming of keys and indexes
# during automatic migrations.

meta = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
      })

Base = declarative_base(metadata=meta)

epicFixVersions = Table('epics_to_versions', Base.metadata, 
    Column('EpicId', ForeignKey('epics.Id')),
    Column('VersionId', ForeignKey('fixversions.Id')))

issueSprints = Table('issues_to_sprints', Base.metadata,
    Column('IssueId', ForeignKey('issues.Id')),
    Column('SprintId', ForeignKey('sprints.Id'))
)

class Epic(Base):
    __tablename__ = 'epics'
    Id = Column(Integer, primary_key=True)
    Date = Column(Date)
    Key = Column(String)
    Summary = Column(String)
    Status = Column(String)
    Issues = relationship('Issue')
    FixVersions = relationship('FixVersion', secondary=epicFixVersions, backref='Epics')

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
    Sprints = relationship('Sprint', secondary=issueSprints, backref='Issues')

class FixVersion(Base):
    __tablename__ = 'fixversions'
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    JiraId = Column(Integer)

class Sprint(Base):
    __tablename__ = 'sprints'
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    JiraId = Column(Integer)

