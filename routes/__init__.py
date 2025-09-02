import json
from flask import Response, request
from app import UnionBanApp
from managers.security_manager import SecurityManager
from structures.responses import BadRequestResponse
from utils.verifying import VerifyingUtils
from werkzeug.exceptions import BadRequest
from . import index
from . import ban_user
from . import unban_user
from . import check_banned
from . import get_bans
from . import get_bans_noverify
from . import review_ban

app = UnionBanApp.get_app()


@app.after_request
async def after_request(response: Response) -> Response:
    response.content_type = 'application/json'
    try:
        response_data = response.get_json()
        if isinstance(response_data, dict) and 'code' in response_data:
            response.status_code = response_data['code']
            data = response_data.get('data', {})
            message = data.get('message', None)
            if message is not None:
                response_data['message'] = message
            response.set_data(json.dumps(response_data))
        
        try:
            request_data = request.get_json()
            password = request_data.get('password')
        except BadRequest:
            response.set_data(str(BadRequestResponse({
                'message': 'No password provided.'
            })))
            response.status_code = 400
            return response
        try:
            await VerifyingUtils.not_none(
                password
            )
        except ValueError as e:
            response.set_data(str(BadRequestResponse({
                'message': str(e)
            })))
            response.status_code = 400
            return response
        if not await SecurityManager.verify_password(password):
            response.set_data(str(BadRequestResponse({
                'message': 'Invalid access password.'
            })))
            response.status_code = 400
            return response
    except (TypeError, json.JSONDecodeError):
        pass
    return response