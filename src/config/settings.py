from dotenv import load_dotenv
from pydantic import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    """Model automatically parses the values in the environmental variables.

    Settings object can then be used throughout codebase without the need to
    commit sensitive information to file.
    """

    # Database connection info
    DB_HOST: str
    DB_PORT: int
    DB_DATABASE: str
    DB_USERNAME: str
    DB_PASSWORD: str

    # Google Firebase configuration
    FIREBASE_APP_ID: str
    FIREBASE_API_KEY: str
    FIREBASE_PROJECT_ID: str

    # Google Service Account Credentials
    GOOGLE_SERVICE_ACCOUNT_PROJECT_ID: str
    GOOGLE_SERVICE_ACCOUNT_PRIVATE_ID: str
    GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY: str
    GOOGLE_SERVICE_ACCOUNT_CLIENT_EMAIL: str
    GOOGLE_SERVICE_ACCOUNT_CLIENT_ID: str
    GOOGLE_SERVICE_ACCOUNT_AUTH_URL: str
    GOOGLE_SERVICE_ACCOUNT_TOKEN_URL: str
    GOOGLE_SERVICE_ACCOUNT_AUTH_PROVIDER_CERT_URL: str
    GOOGLE_SERVICE_ACCOUNT_CLIENT_CERT_URL: str


settings = Settings()
