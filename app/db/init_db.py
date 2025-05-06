from sqlalchemy.orm import Session
from . import models, database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """
    Initialize the database by creating all tables
    """
    logger.info("Creating database tables...")
    models.Base.metadata.create_all(bind=database.engine)
    logger.info("Database tables created successfully")

    # Here you could also add code to create initial data
    # such as admin users, default templates, etc.

if __name__ == "__main__":
    init_db() 