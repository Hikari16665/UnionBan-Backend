from flask import request
from app import UnionBanApp
from managers.ban_manager import BanManager
from managers.security_manager import SecurityManager
from structures.responses import BadRequestResponse, SuccessResponse
from utils.verifying import VerifyingUtils


app = UnionBanApp.get_app()

@app.route('/review_ban', methods=['POST'])
async def review_ban() -> str:
    data = request.get_json()
    
    ban_id = data.get('ban_id')
    
    try:
        await VerifyingUtils.not_none(
            ban_id
        )
    except ValueError as e:
        return str(BadRequestResponse({
            'message': str(e)
        }))
    if await BanManager.review_ban(ban_id):
        return str(SuccessResponse({
            'message': 'Ban reviewed.'
        }))
    else:
        return str(BadRequestResponse({
            'message': 'Ban not found.'
        }))
