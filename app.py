
from flask import Flask
from flask_cors import CORS


class UnionBanApp:
    app = Flask('UnionBanApp')
    CORS(app)
    @classmethod
    def get_app(cls) -> Flask:
        return cls.app
