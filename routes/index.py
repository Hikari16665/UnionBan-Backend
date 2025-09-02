from app import UnionBanApp
from structures.responses import SuccessResponse


app = UnionBanApp.get_app()


@app.route('/')
async def index() -> str:
    return str(SuccessResponse({'server': 'running'}))