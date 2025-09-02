ACCESS_PASSWORD = 'dev'

class SecurityManager:
    def __init__(self) -> None:
        pass
    
    @classmethod
    async def verify_password(cls, password: str) -> bool:
        return password == ACCESS_PASSWORD
