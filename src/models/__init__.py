import logging
from src.models.base import get_session, set_session
from src.models.user import UserModel
from src.models.project import Project

try:
    set_session()
except Exception as e:
    logging.error(e.args)
    logging.error("You have some problems with database")
