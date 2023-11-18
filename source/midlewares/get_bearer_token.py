from fastapi import HTTPException, Depends, status
from fastapi.security import (
    OAuth2PasswordBearer,
)
from typing import Annotated
from services.jwt_token import verify_token
from schemas.index import TokenDataSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
async def get_current_bearer_token( token: Annotated[str, Depends(oauth2_scheme)]) -> TokenDataSchema:
    authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    return verify_token(token, credentials_exception)
