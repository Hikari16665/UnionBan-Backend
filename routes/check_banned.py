
import json
from flask import request
from app import UnionBanApp
from managers.ban_manager import BanManager
from structures.responses import BadRequestResponse, SuccessResponse
from utils.verifying import VerifyingUtils


app = UnionBanApp.get_app()

@app.route('/check_banned', methods=['POST'])
async def check_banned() -> str:
    data = request.get_json()
    username = data.get('username')
    try:
        await VerifyingUtils.not_none(username)
    except ValueError as e:
        return str(BadRequestResponse({'message': str(e)}))
    
    if await BanManager.check_player_banned(username):
        result = {'result': True}
        ban = await BanManager.get_ban_info(username)
        for key, value in json.loads(ban.json()).items():
            result[key] = value
        return str(SuccessResponse(result))
    else:
        return str(SuccessResponse({'result': False}))
    
