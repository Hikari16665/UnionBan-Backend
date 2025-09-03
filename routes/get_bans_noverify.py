import json

from flask import request
from app import UnionBanApp
from managers.ban_manager import BanManager
from managers.security_manager import SecurityManager
from structures.responses import BadRequestResponse, SuccessResponse
from utils.verifying import VerifyingUtils


app = UnionBanApp.get_app()

@app.route('/get_bans_noverify', methods=['POST'])
async def get_bans_noverify() -> str:


    await BanManager.reload_bans()
    return str(SuccessResponse({
        'bans': [json.loads(ban.json()) for ban in BanManager.bans if not ban.reviewed]
    }))
