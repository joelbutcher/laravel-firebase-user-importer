from firebase_admin import auth


def get_hash_alg() -> auth.UserImportHash:
    """The hashing algorithm used to hash passwords in your Laravel database. By default,
    Laravel hashes password using the "bcrypt" algorithm, however this may change. You
    are free to use any of the instances supported in the Firebase Auth SDK.

    Current methods available:
        "hmac_sha512", "hmac_sha256", "hmac_sha1", "hmac_md5",
        "md5", "sha1", "sha256", "sha512", "pbkdf_sha1",
        "pbkdf2_sha256" "scrypt", "bcrypt" and
        "standard_scrypt"
    """
    return auth.UserImportHash.bcrypt()