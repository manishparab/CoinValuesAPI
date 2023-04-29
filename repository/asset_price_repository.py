from typing import Awaitable

import psycopg2
from model.asset import Asset
from model.asset_price import AssetPrice
from repository.database.connection_pool import pool
import asyncio


class AssetPriceRepository:

    @staticmethod
    async def get_asset_prices_record_count() -> Awaitable[int]:
        conn = None
        try:
            conn = pool.getconn()
            with conn.cursor() as cur:
                query: str = "select count(1) as total_count from crypto.asset_price"
                cur.execute(query)
                record = cur.fetchone()
                if record is not None:
                    return record["total_count"]
                else:
                    return 0
        except (Exception, psycopg2.DatabaseError) as error:
            raise error
        finally:
            if conn is not None:
                pool.putconn(conn)

    @staticmethod
    async def insert_assets_prices(asset_price_list: list[AssetPrice]):
        conn = None
        try:
            conn = pool.getconn()
            for asset_price in asset_price_list:
                with conn.cursor() as cur:
                    insert_record = 'insert into crypto.asset_price (asset_id,price_usd,time) ' \
                                    'VALUES (%s, %s, %s);'
                    insert_value = (asset_price.id, asset_price.priceUsd, asset_price.time)
                    cur.execute(insert_record, insert_value)
            conn.commit()
        except Exception as error:
            raise error
        finally:
            if conn is not None:
                pool.putconn(conn)

    @staticmethod
    async def get_assets() -> Awaitable[list[Asset]]:
        conn = None
        try:
            assets: list[Asset] = []
            conn = pool.getconn()
            with conn.cursor() as cur:
                cur.execute('select * from crypto.asset')
                for record in cur.fetchall():
                    assets.append(Asset(record["asset_id"], record["name"]))
            return assets
        except (Exception, psycopg2.DatabaseError) as error:
            raise error
        finally:
            if conn is not None:
                pool.putconn(conn)

    @staticmethod
    async def get_asset_by_id(asset_id: str) -> Awaitable[Asset]:
        conn = None
        try:
            conn = pool.getconn()
            with conn.cursor() as cur:
                cur.execute('select * from crypto.asset where asset_id = %(asset_id)s', {"asset_id": asset_id})
                record = cur.fetchone()
            return Asset(record["asset_id"], record["name"])
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                pool.putconn(conn)

    #  this method gets price at interval, like 1 hr, 4 hr, 8 hr.ect
    #  I have added delta of 5 mins , so we price from between (Interval , Interval + 5 mins)
    @staticmethod
    async def get_assets_price_for_interval(asset_id: str, interval: int) -> Awaitable[float]:
        conn = None
        try:
            conn = pool.getconn()
            with conn.cursor() as cur:
                query: str = ""
                if interval is not None:
                    query = "select price_usd from crypto.asset_price " \
                            "where asset_id = %(asset_id)s " \
                            "and (time >= ((extract(epoch from now())) -60*60* {0})  " \
                            "and time <= (extract(epoch from now()) - (60*60*{0})+(60*5))) " \
                            "order by time limit 1".format(interval)
                else:
                    query = "select price_usd from crypto.asset_price " \
                            "where asset_id = %(asset_id)s " \
                            "order by time desc limit 1"

                cur.execute(query, {"asset_id": asset_id})
                record = cur.fetchone()
                if record is not None:
                    return record["price_usd"]
                else:
                    return None
        except (Exception, psycopg2.DatabaseError) as error:
            raise error
        finally:
            if conn is not None:
                pool.putconn(conn)
