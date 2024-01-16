from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from django.conf import settings
from jwt_auth.models import User
from jwt_auth.schemas import Token


class Hasher:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def check_user_is_allowed(cls, password: str, user: User):
        if cls.verify_password(password, user.hashed_password):
            return True

        return False


class JWTMiddleware:
    ALGORITHM = "HS256"
    ACCESS_TOKEN_KEY = settings.SECRET_KEY
    REFRESH_TOKEN_KEY = settings.REFRESH_TOKEN_SECRET_KEY
    ACCESS_TOKEN_EXP = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    REFRESH_TOKEN_EXP = settings.REFRESH_TOKEN_EXPIRE_MINUTES

    @classmethod
    def encode(cls, sub: Any, key: str, expire_period: int):
        expire = datetime.utcnow() + timedelta(minutes=expire_period)
        return jwt.encode({"exp": expire, "sub": str(sub)}, key, algorithm=cls.ALGORITHM)

    @classmethod
    def get_all_new_tokens(cls, id: int) -> Token:
        acc_tkn = cls.encode(sub=id, key=cls.ACCESS_TOKEN_KEY,
                             expire_period=cls.ACCESS_TOKEN_EXP)
        ref_tkn = cls.encode(sub=id, key=cls.REFRESH_TOKEN_KEY,
                             expire_period=cls.REFRESH_TOKEN_EXP)
        return Token(access_token=acc_tkn, refresh_token=ref_tkn, token_type="bearer")

    @classmethod
    def create_access_token(
        cls,
        subject: Union[str, Any],
    ) -> str:
        return cls.encode(sub=subject, key=cls.ACCESS_TOKEN_KEY, expire_period=cls.ACCESS_TOKEN_EXP)

    @classmethod
    def decode_token(
        cls,
        token: str
    ):
        try:
            user_id = jwt.decode(token, cls.REFRESH_TOKEN_KEY,
                                 cls.ALGORITHM).get('sub', None)
        except:
            return False

        return cls.create_access_token(user_id)

    @classmethod
    def verify_token(
        cls,
        token: str
    ):
        try:
            jwt.decode(token, cls.ACCESS_TOKEN_KEY, cls.ALGORITHM)
            return True
        except:
            return False
