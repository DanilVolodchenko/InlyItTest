import uvicorn
from loguru import logger

from .config import settings
from .app import create_app
from .config import settings
from .utils import do_migrate

logger.add('log/file_{time:DD-MM-YYYY}.log', retention=7, level='INFO')

__version__ = (0, 0, 0)


def main() -> None:
    logger.info(f'Запуск приложения c версией, {".".join(map(str, __version__))}')
    do_migrate()

    app = create_app(__version__)

    uvicorn.run(app, host=settings.LOCAL_SERVER_HOST, port=settings.LOCAL_SERVER_PORT)
