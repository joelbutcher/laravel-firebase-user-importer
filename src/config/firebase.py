from firebase_admin.credentials import Certificate

from src.config.settings import settings


def build_firebase_credentials() -> Certificate:
    return Certificate({
        "type": "service_account",
        "project_id": settings.GOOGLE_SERVICE_ACCOUNT_PROJECT_ID,
        "private_key_id": settings.GOOGLE_SERVICE_ACCOUNT_PRIVATE_ID,
        "private_key": settings.GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY,
        "client_email": settings.GOOGLE_SERVICE_ACCOUNT_CLIENT_EMAIL,
        "client_id": settings.GOOGLE_SERVICE_ACCOUNT_CLIENT_ID,
        "auth_uri": settings.GOOGLE_SERVICE_ACCOUNT_AUTH_URL,
        "token_uri": settings.GOOGLE_SERVICE_ACCOUNT_TOKEN_URL,
        "auth_provider_x509_cert_url": settings.GOOGLE_SERVICE_ACCOUNT_AUTH_PROVIDER_CERT_URL,
        "client_x509_cert_url": settings.GOOGLE_SERVICE_ACCOUNT_CLIENT_CERT_URL
    })