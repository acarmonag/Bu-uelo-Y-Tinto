import re
from dataclasses import dataclass

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from config.config import Config
from lib.Shared.domain.errors.DomainError import ValidationError

SECRET_KEY = bytes.fromhex(Config.load_from_env().secret_key)
SECRET_IV = bytes.fromhex(Config.load_from_env().secret_iv)

pattern = r"^[A-Za-z\d@$!%*?&#.]{8,}$"


@dataclass(frozen=True)
class BasePassword:
    encrypted_value: bytes
    value: str = None

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise ValidationError("Value must be a string")
        if len(self.value) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', self.value):
            raise ValidationError("Password must contain at least one letter and one number")

    @staticmethod
    def _is_valid_password(password: str) -> bool:
        return bool(re.match(pattern, password))

    @staticmethod
    def get_pattern() -> str:
        return pattern

    def get_decrypted(self) -> str:
        cipher = Cipher(
            algorithms.AES(SECRET_KEY), modes.CBC(SECRET_IV), backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded = decryptor.update(self.encrypted_value) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded) + unpadder.finalize()
        object.__setattr__(self, "value", data.decode())
        return self.value

    @classmethod
    def create(cls, plain_password: str) -> "BasePassword":
        if not cls._is_valid_password(plain_password):
            raise ValidationError("Invalid password format")

        padder = padding.PKCS7(128).padder()
        data = padder.update(plain_password.encode()) + padder.finalize()

        cipher = Cipher(
            algorithms.AES(SECRET_KEY), modes.CBC(SECRET_IV), backend=default_backend()
        )
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(data) + encryptor.finalize()
        return cls(encrypted)

    def verify(self, plain_password: str) -> bool:
        return self.get_decrypted() == plain_password

    def equals(self, other: "BasePassword") -> bool:
        return self.get_decrypted() == other.get_decrypted()
