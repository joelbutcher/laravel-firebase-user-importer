from src.config.settings import settings
from src.models.database import Database


# Create the database connection
database = Database(
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_DATABASE,
    username=settings.DB_USERNAME,
    password=settings.DB_PASSWORD
)