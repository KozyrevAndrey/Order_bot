import asyncpg
from asyncpg.pool import Pool

from typing import Union
from datetime import date

from data import config



class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        pool = await asyncpg.create_pool(
            user=config.PGUSER,
            password=config.PGPASSWORD,
            host=config.ip,
            database=config.DATABASE
        )
        self.pool = pool


    # Table for users
    async def create_table_users(self):
        sql = """CREATE TABLE IF NOT EXISTS users(
        id serial PRIMARY KEY,
        id_tlg int,
        fullname varchar(64),
        user_name varchar(64) DEFAULT NULL
        );
        """
        await self.pool.execute(sql)

    # Table for pvz
    async def create_table_pvz(self):
        sql = """CREATE TABLE IF NOT EXISTS pvz(
        id serial,
        pvz_name varchar(16) PRIMARY KEY
        );
        """
        await self.pool.execute(sql)


    # Table for accepted orders
    async def create_table_d_acc(self):
        sql = """
        CREATE TABLE IF NOT EXISTS orders_kzn_acc(
        id serial,
        f_pvz varchar(16) REFERENCES pvz(pvz_name),
        amount int,
        insert_day date DEFAULT CURRENT_DATE
        );
        """
        await self.pool.execute(sql)

    # Table for given orders
    async def create_table_d_g(self):
        sql = """CREATE TABLE IF NOT EXISTS orders_kzn_give(
        id serial,
        f_pvz varchar(16) REFERENCES pvz(pvz_name),
        amount int,
        insert_day date DEFAULT CURRENT_DATE
        );
        """
        await self.pool.execute(sql)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters, start=1)
        ]
        )
        return sql, tuple(parameters.values())

    async def add_users(self, id_tlg: int, fullname: str, user_name: str = None):
        sql = "INSERT INTO users(id_tlg, fullname, user_name) VALUES ($1, $2, $3)"
        await self.pool.execute(sql, id_tlg, fullname, user_name)

    async def add_orders(self, pvz: str, amount: int):
        sql = "INSERT INTO orders_kzn_days(pvz, amount) VALUES ($1, $2)"
        await self.pool.execute(sql, pvz, amount)

    async def add_orders_acc(self, f_pvz: str, amount: int):
        sql = "INSERT INTO orders_kzn_acc(f_pvz, amount) VALUES ($1, $2)"
        await self.pool.execute(sql, f_pvz, amount)

    async def add_orders_given(self, f_pvz: str, amount: int):
        sql = "INSERT INTO orders_kzn_give(f_pvz, amount) VALUES ($1, $2)"
        await self.pool.execute(sql, f_pvz, amount)


    async def select_orders_acc(self, f_pvz: str, insert_day: date):
        sql = "SELECT amount FROM orders_kzn_acc WHERE f_pvz = $1 AND insert_day = $2"
        return await self.pool.fetchval(sql, f_pvz, insert_day)

    async def select_orders_given(self, f_pvz: str, insert_day: date):
        sql = "SELECT amount FROM orders_kzn_d_g WHERE f_pvz = $1 AND insert_day = $2"
        return await self.pool.fetchval(sql, f_pvz, insert_day)


    async def count_orders(self):
        sql = "SELECT SUM(amount) FROM orders_kzn_acc"
        return await self.pool.fetchval(sql)

    async def select_all(self):
        sql = "SELECT * FROM orders_kzn_days"
        return await self.pool.fetch(sql)







