import secrets

from app.auth.hasher import hash_password, verify_password


class TestHasher:
    password = secrets.token_urlsafe(16)
    hashed_password = hash_password(password)
    wrong_password = secrets.token_urlsafe(17)

    def test_hash_password_positive(self) -> None:
        assert verify_password(
            self.password, self.hashed_password
        ), "Password is not correct"

    def test_hash_password_negative(self) -> None:
        assert not verify_password(
            self.wrong_password, self.hashed_password
        ), "Password is correct"
