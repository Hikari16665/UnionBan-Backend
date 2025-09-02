from flask import request
from app import UnionBanApp
from managers.ban_manager import BanManager
from managers.security_manager import SecurityManager
from structures.responses import BadRequestResponse, NoContentResponse, SuccessResponse
from utils.verifying import VerifyingUtils


app = UnionBanApp.get_app()

@app.route('/unban_user', methods=['POST'])
async def unban_user() -> str:
    
    data = request.get_json()
    
    password = data.get('password')
    username = data.get('username')
    
    try:
        await VerifyingUtils.not_none(password, username)
    except ValueError as e:
        return str(BadRequestResponse({'message': str(e)}))
    
    if not await SecurityManager.verify_password(password):
        return str(BadRequestResponse({'message': 'Invalid access password'}))
    
    if await BanManager.unban_user(username):
        return str(SuccessResponse({'message': 'User unbanned'}))
    else:
        return str(NoContentResponse({'message': 'User not found'}))
