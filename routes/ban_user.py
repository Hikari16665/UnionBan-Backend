import datetime

from flask import request
from app import UnionBanApp
from managers.ban_manager import BanManager
from managers.security_manager import SecurityManager
from structures.responses import BadRequestResponse, SuccessResponse
from utils.verifying import VerifyingUtils


app = UnionBanApp.get_app()

@app.route('/ban_user', methods=['POST'])
async def ban_user() -> str:
    data = request.get_json()
    
    
    
    password = data.get('password')
    username = data.get('username')
    reason = data.get('reason')
    server = data.get('server')
    created_by = data.get('created_by')
    expires_at = data.get('expires_at')
    is_permanent = data.get('is_permanent')
    
    try:
        await VerifyingUtils.not_none(
            password,
            username,
            reason,
            server,
            created_by,
            is_permanent,
        )
    except ValueError as e:
        return str(BadRequestResponse({'message': str(e)}))
    
    if not await SecurityManager.verify_password(password):
        return str(BadRequestResponse({'message': 'Invalid access password'}))
    
    if is_permanent:
        expires_at = None
    
    if expires_at is not None:
        expires_at_date = datetime.datetime.fromisoformat(expires_at)
    else:
        expires_at_date = None
    
    await BanManager.ban_user(
        username,
        reason,
        server,
        created_by,
        datetime.datetime.now(),
        expires_at_date,
        is_permanent
    )
    
    return str(SuccessResponse({'message': 'User banned'}))