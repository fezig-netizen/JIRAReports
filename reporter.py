from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config
from models import Epic, Issue

cfg = Config()
engine = create_engine(cfg.DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

