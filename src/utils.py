import os

from fastapi import Depends
from alembic import config, command
from loguru import logger

from .services import UserService
from .security import access_token
from .models.dto.roles import Roles
from .exceptions import PermissionDenied
from .config import settings


def admin_required(token: str = Depends(access_token)) -> None:
    user = UserService.get_current_user(token)
    if user.role != Roles.admin:
        raise PermissionDenied('Недостаточно прав')


def do_migrate() -> None:
    try:
        logger.info('Применение миграций БД')
        cfg = _alembic_cfg()
        command.upgrade(cfg, 'head')
        logger.success('Миграции успешно выполнены')
    except Exception as exc:
        logger.error(f'Ошибка применения миграций: {exc}')
        raise exc


def _alembic_cfg() -> config.Config:
    cfg = config.Config()
    cfg.set_main_option('script_location', os.path.join(os.getcwd(), 'migrations'))
    cfg.set_main_option('version_path_separator', 'os')
    cfg.set_main_option('sqlalchemy.url', settings.db_connection_string)
    cfg.set_main_option('prepend_sys_path', '.')
    return cfg
