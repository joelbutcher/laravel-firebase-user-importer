import firebase_admin
import pymysql
from firebase_admin import auth, exceptions
from firebase_admin.auth import UserNotFoundError, UserRecord

from src.config.database import database
from src.config.firebase import build_firebase_credentials
from src.config.hashing import get_hash_alg
from src.config.settings import settings

per_page: int = 100


def calculate_offset(
        page: int = 1
) -> int:
    return (page - 1) * per_page


def fetch_page(
        connection: pymysql.connect,
        page: int = 1,
) -> tuple:
    offset = calculate_offset(page)

    with connection.cursor() as cursor:
        cursor.execute(
            query=f"SELECT * FROM {settings.DB_DATABASE}.users LIMIT {per_page} OFFSET {offset}"
        )

        return cursor.fetchall()


def user_exists_for_email(email) -> bool:
    """Does a lookup for the given email address to determine if there is
        already a record for in firestore.
    """
    try:
        user = auth.get_user_by_email(email)
        if isinstance(user, UserRecord):
            return user.email == email
    except UserNotFoundError:
        return False
    except exceptions.FirebaseError:
        # Some unrecoverable error occurred that prevented the operation from running.
        pass


def import_page(
        users: tuple
):
    import_batch = []
    for user in users:
        uid = user["firebase_uid"]
        name = user["name"]
        email = user["email"]
        password = user["password"]
        password_hash = f"{password}".encode("ascii")

        # Only import the users if one doesn't already exist for that email
        if not user_exists_for_email(email):
            import_batch.append(
                auth.ImportUserRecord(
                    uid=uid,
                    display_name=name,
                    email=email,
                    password_hash=password_hash
                )
            )

    print("Importing {0} users".format(len(import_batch)))

    if len(import_batch) > 0:
        hash_alg = get_hash_alg()

        try:
            result = auth.import_users(users=import_batch, hash_alg=hash_alg)
            print("Successfully imported {0} users. Failed to import {1} users.".format(
                result.success_count, result.failure_count))
            for err in result.errors:
                print("Failed to import {0} due to {1}".format(users[err.index].uid, err.reason))
        except exceptions.FirebaseError:
            # Some unrecoverable error occurred that prevented the operation from running.
            pass


def import_users(
        connection: pymysql.connect,
        page: int = 1,
) -> None:
    current_page = fetch_page(connection, page)

    # Only import if we have users to import
    if len(current_page) > 0:
        import_page(users=current_page)

        # Continue to the next page if we've hit the page limit
        # for the current page
        if len(current_page) == per_page:
            import_users(connection, page + 1)


def main():
    firebase_admin.initialize_app(build_firebase_credentials(), {
        "appId": settings.FIREBASE_APP_ID,
        "apiKey": settings.FIREBASE_API_KEY,
        "projectId": settings.FIREBASE_PROJECT_ID,
    })

    connection = database.new_connection()

    import_users(
        connection=connection
    )


if __name__ == '__main__':
    main()
