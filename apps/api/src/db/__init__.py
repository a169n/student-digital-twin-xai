from src.db.models import Base
from src.db.session import get_engine


def init_db() -> None:
    Base.metadata.create_all(bind=get_engine())
