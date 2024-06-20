from datetime import timedelta, datetime

import dotenv
import jwt
from dotenv import load_dotenv

from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.user_repisitory import UserRepository
from schemas.user_schema import UserInput, UserOutput, Token

from config.database import Session

load_dotenv()

_bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class AuthServiceUtils(metaclass=SingletonMeta):
    __SECRET_KEY = dotenv.get_key(".env", "JWT_SECRET")
    __ALGHORITM = dotenv.get_key(".env", "ALGORITHM")
    __EXPIRES_IN_ACCESS_TOKEN = timedelta(minutes=15)
    __EXPIRES_IN_REFRESH_TOKEN = timedelta(days=3)
    __TOKEN_TYPE = "type"
    _instances = {}

    def __init__(self, session: AsyncSession):
        self._user_repository = UserRepository(session)

    def create_access_token(self, user: UserOutput, expires_delta: timedelta) -> str:
        print(user)
        to_encode = {
            self.__TOKEN_TYPE: "access",
            "sub": user.email,
            "id": user.id,
            "role": user.role,
            "exp": datetime.utcnow() + expires_delta,
            "iat": datetime.utcnow()
        }

        return jwt.encode(to_encode, self.__SECRET_KEY, algorithm=self.__ALGHORITM)

    def create_refresh_token(self, user: UserOutput, expires_delta: timedelta) -> str:
        to_encode = {
            self.__TOKEN_TYPE: "refresh",
            "sub": user.email,
            "id": user.id,
            "role": user.role,
            "exp": datetime.utcnow() + expires_delta,
            "iat": datetime.utcnow()
        }

        return jwt.encode(to_encode, self.__SECRET_KEY, algorithm=self.__ALGHORITM)

    def get_token_payload(self, token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, self.__SECRET_KEY, algorithms=[self.__ALGHORITM])
            return payload
        except PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def type_token_is(self, payload: dict, token_type: str) -> bool:
        token_type_from_payload = payload.get(self.__TOKEN_TYPE)

        if token_type_from_payload == token_type:
            return True

        return False

    async def get_user_by_payload(self, payload: dict) -> UserOutput | None:
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return await self._user_repository.get_by_id(user_id)

    def authenticate_user_from_token_type(self, token_type: str):
        async def get_auth_user(payload: dict = Depends(self.get_token_payload)) -> UserOutput:
            if not self.type_token_is(payload, token_type):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return await self.get_user_by_payload(payload)

        return get_auth_user

    async def authenticate_user(self, email: str, password: str) -> UserOutput | bool:
        unauthorized_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

        user = await self._user_repository.get_user({"email": email})
        if user is None:
            raise unauthorized_exception
        if not _bcrypt_context.verify(password, user.password):
            raise unauthorized_exception

        return user


_auth_service_utils = AuthServiceUtils(Session())
_auth_cur_user_access = _auth_service_utils.authenticate_user_from_token_type("access")
_auth_cur_user_refresh = _auth_service_utils.authenticate_user_from_token_type("refresh")


class AuthService(metaclass=SingletonMeta):
    def __init__(self):
        self.__EXPIRES_IN_ACCESS_TOKEN = timedelta(minutes=15)
        self.__EXPIRES_IN_REFRESH_TOKEN = timedelta(days=3)

    async def role_check(self, roles: list[str], user: UserOutput = Depends(_auth_cur_user_access)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient privileges",
            )
        return user

    async def refresh_token(self, _user: UserOutput = Depends(_auth_cur_user_refresh)) -> Token | None:
        access_token = _auth_service_utils.create_access_token(_user, self.__EXPIRES_IN_ACCESS_TOKEN)
        refresh_token = _auth_service_utils.create_refresh_token(_user, self.__EXPIRES_IN_REFRESH_TOKEN)
        return Token(
            access_token=access_token,
            refresh_token=refresh_token
        )

    async def login(self, email: str, password: str) -> Token | None:
        if email == "" or password == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Имя или пароль не были заполнены",
            )

        user = await _auth_service_utils.authenticate_user(email, password)
        access_token = _auth_service_utils.create_access_token(user, self.__EXPIRES_IN_ACCESS_TOKEN)
        refresh_token = _auth_service_utils.create_refresh_token(user, self.__EXPIRES_IN_REFRESH_TOKEN)
        return Token(access_token=access_token, refresh_token=refresh_token)


    async def register_user(self, user: UserInput) -> UserOutput:
        is_exist_user = await _auth_service_utils._user_repository.get_user({"email": user.username})
        if is_exist_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists",
            )
        user.password = _bcrypt_context.hash(user.password)
        return await _auth_service_utils._user_repository.create(user.__dict__)

    def role_req(self, *roles: str):
        async def check(user: UserOutput = Depends(_auth_cur_user_access)):
            return await self.role_check(list(roles), user)

        return check




