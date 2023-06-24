import os


import sqlalchemy
from sqlalchemy.orm import sessionmaker

from auth.auth import true_pass
from config import path_to_env
from tool_db import create_row, get_row, delete_row, patch_row, get_row_addr
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine

from uvicorn import run
from models import Post_Item, Delete_item, Addr_item, Address_table, DeclarativeBase, Patch_Item, Get_item

load_dotenv(path_to_env)

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


@app.post("/address/")
async def create_item(item: Post_Item):
    if not true_pass(item.password):
        raise HTTPException(status_code=401, detail="Unauthorized.")
    ans = create_row(item, session)
    if isinstance(ans, sqlalchemy.exc.IntegrityError):
        raise HTTPException(status_code=400, detail="The value 'addr_init' is already present in the database.")
    elif isinstance(ans, Exception):
        raise HTTPException(status_code=500, detail=str(ans))
    return 'A new row has been created successfully.'


@app.get("/address/")
async def root(data: Get_item):
    if not true_pass(data.password):
        raise HTTPException(status_code=401, detail="Unauthorized.")
    ans = get_row(data.row_id, session)
    if isinstance(ans, KeyError):
        raise HTTPException(status_code=400, detail="There is no such 'row_id'.")
    elif isinstance(ans, Exception):
        raise HTTPException(status_code=500, detail=str(ans))
    return ans


@app.delete("/address/")
async def delete_item(data: Delete_item):
    if not true_pass(data.password):
        raise HTTPException(status_code=401, detail="Unauthorized.")
    ans = delete_row(data.row_id, session)
    if isinstance(ans, KeyError):
        raise HTTPException(status_code=400, detail="There is no such 'row_id'.")
    elif isinstance(ans, Exception):
        raise HTTPException(status_code=500, detail=str(ans))
    else:
        return "The deletion was successful."


@app.patch("/address/")
async def patch_item(data: Patch_Item):
    if not true_pass(data.password):
        raise HTTPException(status_code=401, detail="Unauthorized.")
    if data.addr_init is not None:
        raise HTTPException(status_code=400, detail="You cannot change the 'addr_init' column.")
    ans = patch_row(data, session)
    if isinstance(ans, KeyError):
        raise HTTPException(status_code=400, detail="There is no such 'row_id'.")
    elif isinstance(ans, Exception):
        raise HTTPException(status_code=500, detail=str(ans))
    return 'Changes have been successfully applied'


@app.get("/address/addr/")
async def get_item_addr(data: Addr_item):
    if not true_pass(data.password):
        raise HTTPException(status_code=401, detail="Unauthorized.")
    ans = get_row_addr(data, session)
    if isinstance(ans, KeyError):
        raise HTTPException(status_code=400, detail="There were no such 'addrs'.")
    elif isinstance(ans, Exception):
        raise HTTPException(status_code=500, detail=str(ans))
    return ans


if __name__ == "__main__":
    run(app)
