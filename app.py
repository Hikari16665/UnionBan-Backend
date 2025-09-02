
from flask import Flask



class UnionBanApp:
    app = Flask('UnionBanApp')
    
    @classmethod
    def get_app(cls) -> Flask:
        return cls.app
