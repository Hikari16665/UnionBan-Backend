import datetime
import logging
from typing import Iterable, Optional
import aiosqlite


DB_FILE = 'database.db'

class DatabaseManager:
    def __init__(self) -> None:
        pass
    
    @classmethod
    async def execute_sql(cls, sql: str, params: tuple = ()) -> int:
        logger = logging.getLogger('database')
        async with aiosqlite.connect(DB_FILE) as db:
            async with db.execute(sql, params) as cursor:
                await db.commit()
                logger.info(f'Executed SQL: {sql} with params {params}, affected {cursor.rowcount} rows.')
                return cursor.rowcount
            
            
    
    @classmethod
    async def create_tables(cls) -> None:
        await cls.execute_sql('''
                               CREATE TABLE IF NOT EXISTS bans (
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   username TEXT,
                                   reason LONGTEXT,
                                   server TEXT,
                                   created_by TEXT,
                                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                   expires_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                   is_permanent BOOLEAN DEFAULT FALSE,
                                   reviewed BOOLEAN DEFAULT FALSE
                               )
                               ''')
    @classmethod
    async def fetch_sql(cls, sql: str, params: tuple = ()) -> Iterable[aiosqlite.Row]:
        async with aiosqlite.connect(DB_FILE) as db:
            async with db.execute(sql, params) as cursor:
                return await cursor.fetchall()



    