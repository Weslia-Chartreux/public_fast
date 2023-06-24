import psycopg2
from sqlalchemy import Column, Integer, String, Float, SMALLINT
from sqlalchemy.orm import sessionmaker

from models import Post_Item, Address_table, Delete_item, Patch_Item, Addr_item


def create_row(item: Post_Item, session):
    try:
        new_row = Address_table(addr_init=item.addr_init,
                                addr_clean=item.addr_clean,
                                addr_dadata=item.addr_dadata,
                                addr_yandex=item.addr_yandex,
                                lat_dadata=item.lat_dadata,
                                lon_dadata=item.lon_dadata,
                                aq_dadata=item.aq_dadata,
                                lat_yandex=item.lat_yandex,
                                lon_yandex=item.lon_yandex)
        session.add(new_row)
        session.commit()
        return 'OK'
    except psycopg2.errors.UniqueViolation as _ex:
        return _ex
    except Exception as _ex:
        return _ex


def get_row(row_id: int, session):
    try:
        ans = session.query(Address_table).filter(Address_table.row_id == row_id).first()
        if ans is None:
            raise KeyError
        return ans
    except Exception as _ex:
        return _ex


def delete_row(row_id: int, session):
    try:
        address = session.query(Address_table).get(row_id)
        if address is None:
            raise KeyError
        session.delete(address)
        session.commit()
        return 'OK'
    except Exception as _ex:
        return _ex


def patch_row(item: Patch_Item, session):
    try:
        address = session.query(Address_table).get(item.row_id)
        if address is None:
            raise KeyError
        address.addr_clean = item.addr_clean if item.addr_clean is not None else address.addr_clean
        address.addr_dadata = item.addr_dadata if item.addr_dadata is not None else address.addr_dadata
        address.addr_yandex = item.addr_yandex if item.addr_yandex is not None else address.addr_yandex
        address.lat_dadata = item.lat_dadata if item.lat_dadata is not None else address.lat_dadata
        address.lon_dadata = item.lon_dadata if item.lon_dadata is not None else address.lon_dadata
        address.aq_dadata = item.aq_dadata if item.aq_dadata is not None else address.aq_dadata
        address.lat_yandex = item.lat_yandex if item.lat_yandex is not None else address.lat_yandex
        address.lon_yandex = item.lon_yandex if item.lon_yandex is not None else address.lon_yandex
        session.commit()
        return 'OK'
    except Exception as _ex:
        return _ex


def get_row_addr(data: Addr_item, session):
    try:
        ans = session.query(Address_table).filter(Address_table.addr_init == data.addr).all() + \
               session.query(Address_table).filter(Address_table.addr_clean == data.addr).all() + \
               session.query(Address_table).filter(Address_table.addr_yandex == data.addr).all() + \
               session.query(Address_table).filter(Address_table.addr_dadata == data.addr).all()
        if not ans:
            raise KeyError
        return list(set(ans))
    except Exception as _ex:
        return _ex
