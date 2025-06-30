from databases.database import engine, Base
from models import *  # This imports all models

Base.metadata.create_all(bind=engine)