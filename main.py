import os

import psycopg2
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from tool_db import create_row, get_row, delete_row, patch_row, get_row_addr
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine

from uvicorn import run
from models import Post_Item, Delete_item, Addr_item, Address_table, DeclarativeBase, Patch_Item
from config import host_asgi, port_asgi
import databases

load_dotenv('111.env')

# берем параметры БД из переменных окружения
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
app = FastAPI()
DeclarativeBase.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

@app.on_event("startup")
async def startup():
    # когда приложение запускается устанавливаем соединение с БД
    engine.connect()


@app.on_event("shutdown")
async def shutdown():
    # когда приложение останавливается разрываем соединение с БД
    engine.disconnect()


@app.post("/address/")
async def create_item(item: Post_Item):
    ans = create_row(item, session)
    if isinstance(ans, sqlalchemy.exc.IntegrityError):
        raise HTTPException(status_code=400, detail="The value 'addr_init' is already present in the database.")
    elif isinstance(ans, Exception):
        raise HTTPException(status_code=500, detail=str(ans))
    return 'A new row has been created successfully.'


@app.get("/address/{row_id}")
async def root(row_id: int):
    ans = get_row(row_id, session)
    if isinstance(ans, KeyError):
        raise HTTPException(status_code=400, detail="There is no such 'row_id'.")
    elif isinstance(ans, Exception):
        raise HTTPException(status_code=500, detail=str(ans))
    return ans


@app.delete("/address/")
async def delete_item(data: Delete_item):
    ans = delete_row(data.row_id, session)
    if isinstance(ans, KeyError):
        raise HTTPException(status_code=400, detail="There is no such 'row_id'.")
    elif isinstance(ans, Exception):
        raise HTTPException(status_code=500, detail=str(ans))
    else:
        return "The deletion was successful."


@app.patch("/address/")
async def patch_item(data: Patch_Item):
    if data.addr_init is not None:
        raise HTTPException(status_code=400, detail="You cannot change the 'addr_init' column.")
    ans = patch_row(data, session)
    if isinstance(ans, KeyError):
        raise HTTPException(status_code=400, detail="There is no such 'row_id'.")
    elif isinstance(ans, Exception):
        raise HTTPException(status_code=500, detail=str(ans))
    return 'Changes have been successfully applied'


@app.get("/address/")
async def get_item_addr(data: Addr_item):
    ans = get_row_addr(data, session)
    if isinstance(ans, KeyError):
        raise HTTPException(status_code=400, detail="There were no such 'addrs'.")
    elif isinstance(ans, Exception):
        raise HTTPException(status_code=500, detail=str(ans))
    return ans

if __name__ == "__main__":
    run(app)
