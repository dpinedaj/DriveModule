import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from libraries.constants import Constants as cts 

cts = cts()
engine = create_engine(cts.DB_URL)
Session = sessionmaker(bind=engine)
session = Session()
