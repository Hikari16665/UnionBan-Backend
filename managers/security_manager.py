from datetime import datetime, timedelta
import logging
import secrets
from typing import Optional

import jwt

logger = logging.getLogger('SecurityManager')

ACCESS_PASSWORD = 'Rvm82XD9w6Dp25qFn6B0'
JWT_SECRET_KEY = secrets.token_hex(32)
JWT_ACCESS_TOKEN_EXPIRES = 60
class SecurityManager:
    def __init__(self) -> None:
        pass
    
    @classmethod
    async def verify_password(cls, password: str) -> bool:
        return password == ACCESS_PASSWORD

    @classmethod
    async def create_access_token(cls, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRES)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm='HS256')
        return encoded_jwt
    
    @classmethod
    async def verify_token(cls, token: str, ip: Optional[str]) -> bool:
        logger.info(f'Login attempt from ip {ip} with token {token}')
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            logger.info(f'Payload: {payload} from ip {ip}')
            return True
        except jwt.PyJWTError:
            return False