from app import UnionBanApp
from managers.ban_manager import BanManager
from structures.responses import SuccessResponse


app = UnionBanApp.get_app()


@app.route('/', methods=['POST'])
async def index() -> str:
    await BanManager.reload_bans()
    return str(SuccessResponse({'server': 'running'}))