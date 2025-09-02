import json
from typing import Optional

class Response:
    code: int
    message: str
    data: Optional[dict] = None

    def __init__(self, code: int, message: str, data: Optional[dict] = None):
        self.code = code
        self.message = message
        self.data = data
    
    def to_dict(self) -> dict:
        return {
            'code': self.code,
            'message': self.message,
            'data': self.data if self.data is not None else {}
        }
    
    def __str__(self) -> str:
        return self.to_json()
    

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

class SuccessResponse(Response):
    code: int = 200
    message: str = 'Success'
    data: Optional[dict] = None
    
    def __init__(self, data: Optional[dict] = None) -> None:
        super().__init__(self.code, self.message, data)

class InternalErrorResponse(Response):
    code: int = 500
    message: str = 'Internal Error'
    data: Optional[dict] = None
    
    def __init__(self, data: Optional[dict] = None) -> None:
        super().__init__(self.code, self.message, data)

class BadRequestResponse(Response):
    code: int = 400
    message: str = 'Bad Request'
    data: Optional[dict] = None
    
    def __init__(self, data: Optional[dict] = None) -> None:
        super().__init__(self.code, self.message, data)

class NotFoundResponse(Response):
    code: int = 404
    message: str = 'Not Found'
    data: Optional[dict] = None
    
    def __init__(self, data: Optional[dict] = None) -> None:
        super().__init__(self.code, self.message, data)

class NoContentResponse(Response):
    code: int = 204
    message: str = 'No Content'
    data: Optional[dict] = None
    
    def __init__(self, data: Optional[dict] = None) -> None:
        super().__init__(self.code, self.message, data)
