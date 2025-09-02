import datetime
from typing import Optional
from managers.database_manager import DatabaseManager
from structures.ban import Ban


class BanManager:
    db: DatabaseManager = DatabaseManager()
    bans: list[Ban] = []
    
    def __init__(self) -> None:
        pass
    
    @classmethod
    async def load_bans(cls) -> None:
        bans = await cls.db.fetch_sql('SELECT * FROM bans')
        for ban in bans:
            cls.bans.append(Ban.from_tuple(tuple(ban)))
    
    @classmethod
    async def reload_bans(cls) -> None:
        cls.bans = []
        await cls.load_bans()


    @classmethod
    async def ban_user(cls,
                         username: str,
                         reason: str,
                         server: str,
                         created_by: str,
                         created_at: Optional[datetime.datetime],
                         expires_at: Optional[datetime.datetime] = None,
                         is_permanent: bool = False
                         ) -> None:
        await cls.db.execute_sql('''
                               INSERT INTO bans (username, reason, server, created_by, created_at, expires_at, is_permanent)
                               VALUES (?, ?, ?, ?, ?, ?, ?)
                               ''',
                               (username, reason, server, created_by, created_at, expires_at, is_permanent))
        await cls.reload_bans()
    
    @classmethod
    async def unban_user(cls, username: str) -> bool:
        affected = await cls.db.execute_sql('''
                               DELETE FROM bans
                               WHERE username = ?
                               ''',
                               (username,))
        await cls.reload_bans()
        return affected > 0

    @classmethod
    async def check_player_banned(cls, username: str) -> bool:
        for ban in cls.bans:
            if ban.username == username:
                if ban.expires_at is None or ban.expires_at > datetime.datetime.now():
                    if ban.reviewed:
                        return True
        return False
    
    @classmethod
    async def get_ban_info(cls, username: str) -> Ban:
        for ban in cls.bans:
            if ban.username == username:
                return ban
        raise ValueError(f'Player {username} is not banned.')