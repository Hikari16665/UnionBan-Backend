import json
from flask import Response, request
from app import UnionBanApp
from managers.security_manager import SecurityManager
from structures.responses import BadRequestResponse
from utils.verifying import VerifyingUtils
from werkzeug.exceptions import BadRequest
from . import index
from . import login
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
        # Set the status code to the code in the response data if it exists.
        response_data = response.get_json()
        if isinstance(response_data, dict) and 'code' in response_data:
            response.status_code = response_data['code']
            # Set the message to the message in the response data if it exists.
            data = response_data.get('data', {})
            message = data.get('message', None)
            if message is not None:
                response_data['message'] = message
            response.set_data(json.dumps(response_data))
        
        #these two routes do not need token
        if request.path in ['/login', '/check_banned']:
            return response
        try:
            request_data = request.get_json()
            token = request_data.get('token')
        except BadRequest:
            response.set_data(str(BadRequestResponse({
                'message': 'No token provided.'
            })))
            response.status_code = 400
            return response
        if not await SecurityManager.verify_token(token, request.remote_addr):
            response.set_data(str(BadRequestResponse({
                'message': 'Invalid token.'
            })))
            response.status_code = 401
            return response
    except (TypeError, json.JSONDecodeError):
        pass
    return response