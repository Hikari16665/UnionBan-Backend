import json
from app import UnionBanApp
from managers.ban_manager import BanManager
from structures.responses import SuccessResponse
from utils.verifying import VerifyingUtils


app = UnionBanApp.get_app()

@app.route('/get_bans', methods=['POST'])
async def get_bans() -> str:

    return str(SuccessResponse({
        'bans': [json.loads(ban.json()) for ban in BanManager.bans]
    }))
