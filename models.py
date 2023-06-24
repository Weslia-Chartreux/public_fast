from pydantic import BaseModel
import sqlalchemy
from sqlalchemy import String, Column, Float, SMALLINT, Integer
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


class Post_Item(BaseModel):
    addr_init: str
    addr_clean: str = None
    addr_dadata: str = None
    addr_yandex: str = None
    lat_dadata: float = None
    lon_dadata: float = None
    aq_dadata: int = None
    lat_yandex: float = None
    lon_yandex: int = None


class Delete_item(BaseModel):
    row_id: int


class Addr_item(BaseModel):
    addr: str


class Patch_Item(BaseModel):
    row_id: int
    addr_init: str = None
    addr_clean: str = None
    addr_dadata: str = None
    addr_yandex: str = None
    lat_dadata: float = None
    lon_dadata: float = None
    aq_dadata: int = None
    lat_yandex: float = None
    lon_yandex: int = None


metadata = sqlalchemy.MetaData()


class Address_table(DeclarativeBase):
    __tablename__ = "shop"

    row_id = Column("row_id", Integer, primary_key=True)
    addr_init = Column("addr_init", String(100), unique=True, index=True)
    addr_clean = Column("addr_clean", String(100))
    addr_dadata = Column("addr_dadata", String(100))
    addr_yandex = Column("addr_yandex", String(100))
    lat_dadata = Column("lat_dadata", Float)
    lon_dadata = Column("lon_dadata", Float)
    aq_dadata = Column("aq_dadata", SMALLINT)
    lat_yandex = Column("lat_yandex", Float)
    lon_yandex = Column("lon_yandex", Float)
