from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine

class Request(SQLModel, table=True):
    id                  : Optional[int]     = Field(default=None, primary_key=True)
    request_id          : Optional[str]     = Field(default=None)
    title               : Optional[str]     = Field(default=None)
    description         : Optional[str]     = Field(default=None)
    requester_name      : Optional[str]     = Field(default=None)
    requester_rating    : Optional[str]     = Field(default=None)
    created_date        : datetime          = Field(default_factory=datetime.utcnow,nullable=False)

sqlite_file_name = "mostaql_offers.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)