import bcrypt


def hash_password(password: str) -> str:
    salt: bytes = bcrypt.gensalt()
    hash_password: bytes = bcrypt.hashpw(password.encode(), salt)
    return hash_password.decode()


def verify_password(password: str, hash_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hash_password.encode())
