ACCESS_PASSWORD = 'Rvm82XD9w6Dp25qFn6B0'

class SecurityManager:
    def __init__(self) -> None:
        pass
    
    @classmethod
    async def verify_password(cls, password: str) -> bool:
        return password == ACCESS_PASSWORD
