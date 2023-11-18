from passlib.context import CryptContext

class Hash:
    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    @classmethod
    def bcript(cls, password: str) -> str:
        """
        Args:
            password (str): The plain-text password to be hashed.

        Returns:
            str: The hashed password.

        """
        return cls.pwd_ctx.hash(password)

    @classmethod
    def verify(cls, hashing_password: str, plain_password: str) -> bool:
        """
        Verifies if the provided plain password matches the hashed password.

        Args:
            hashing_password (str): The hashed password to be compared.
            plain_password (str): The plain password to be verified.

        Returns:
            bool: True if the plain password matches the hashed password. False otherwise.
        """
        return cls.pwd_ctx.verify(plain_password, hashing_password)
