from flask import request
from app import UnionBanApp
from managers.security_manager import JWT_ACCESS_TOKEN_EXPIRES, SecurityManager
from structures.responses import BadRequestResponse, SuccessResponse
from utils.verifying import VerifyingUtils


app = UnionBanApp.get_app()

@app.route('/login', methods=['POST'])
async def login() -> str:
    data = request.get_json()
    
    password = data.get('password')
    
    try:
        await VerifyingUtils.not_none(password)
    except ValueError as e:
        return str(BadRequestResponse({'message': str(e)}))
    
    if not await SecurityManager.verify_password(password):
        return str(BadRequestResponse({'message': 'Invalid password'}))
    
    access_token = await SecurityManager.create_access_token(data={"sub": "admin"})
    return str(SuccessResponse({
        'access_token': access_token,
        'token_type': 'payload',
        'expires_in': JWT_ACCESS_TOKEN_EXPIRES
    }))