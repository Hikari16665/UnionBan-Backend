import datetime
from typing import Optional
from pydantic import BaseModel


class Ban(BaseModel):
    id: int
    username: str
    reason: str
    server: str
    created_by: str
    created_at: datetime.datetime
    expires_at: Optional[datetime.datetime] = None
    is_permanent: bool = False
    reviewed: bool = False
    
    def still_active(self) -> bool:
        if self.is_permanent:
            return True
        if self.expires_at is None:
            return True
        return self.expires_at > datetime.datetime.now()
    
    @classmethod
    def from_tuple(cls, data: tuple) -> 'Ban':
        created_at = datetime.datetime.fromisoformat(data[5])
        expires_at = datetime.datetime.fromisoformat(data[6]) if data[6] is not None else None
        is_permanent = data[7] == 1
        reviewed = data[8] == 1

        return cls(
            id=data[0],
            username=data[1],
            reason=data[2],
            server=data[3],
            created_by=data[4],
            created_at=created_at,
            expires_at=expires_at,
            is_permanent=is_permanent,
            reviewed=reviewed
        )
