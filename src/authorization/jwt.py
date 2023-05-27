from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from src.authorization.jwt_handler import decode_jwt_token
from src.exceptions.authentication import AuthenticationException
from src.exceptions.authentication import InvalidTokenException
from src.exceptions.authentication import TokenExpiredException


class JWTBearer(HTTPBearer):
    """Модуль для авторизации"""
    valid_schemas = ["Bearer"]

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=False)

    async def __call__(self, request: Request):
        token: HTTPAuthorizationCredentials = await super().__call__(request)
        if not token:
            raise AuthenticationException(
                status_code=400, message="Authorization token doesn't received."
            )
        if token.scheme not in self.valid_schemas:
            raise InvalidTokenException(status_code=401, message="Invalid token schema.")
        if not token.credentials:
            raise InvalidTokenException(status_code=401, message="Token not transferred")

        is_valid, user_id = decode_jwt_token(token.credentials)

        if is_valid:
            request.state.user_id = user_id
            return token
            # return await call_next(request)

        raise TokenExpiredException(
            status_code=401, message="Signature expired. Please log in again."
        )
