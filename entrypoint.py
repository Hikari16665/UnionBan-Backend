from routes import *
import asyncio
import logging
from logging import Logger
from app import UnionBanApp
from managers.ban_manager import BanManager, DatabaseManager

app = UnionBanApp.get_app()

async def run_app(logger: Logger) -> None:
    logger.info('Starting UnionBan...')
    logger.info('Initializing Database...')
    await DatabaseManager.create_tables()
    logger.info('Database initialized.')
    
    logger.info('Loading bans...')
    await BanManager.load_bans()
    logger.info(f'{len(BanManager.bans)} bans loaded.')
    logger.info('Starting server...')
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(name)s][%(levelname)s] - %(message)s')
    logger = logging.getLogger('UnionBan')
    asyncio.run(run_app(logger))
    
    
