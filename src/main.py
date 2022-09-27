import firebase_admin

from src.config.database import database
from src.config.firebase import build_firebase_credentials
from src.config.settings import settings
from src.logic.functions import import_users

firebase_admin.initialize_app(
    build_firebase_credentials(),
    {
        "appId": settings.FIREBASE_APP_ID,
        "apiKey": settings.FIREBASE_API_KEY,
        "projectId": settings.FIREBASE_PROJECT_ID,
    },
)

connection = database.new_connection()

import_users(connection=connection)
