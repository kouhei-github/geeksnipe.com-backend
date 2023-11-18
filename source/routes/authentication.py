import boto3, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.index import LoginSchema, UserOut, UserAuth
from config.index import get_db
from models.index import User
from services.jwt_token import create_access_token, verify_password, create_refresh_token, get_hashed_password
from schemas.index import TokenSchema

auth = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)

@auth.post('/signup', status_code=status.HTTP_201_CREATED, summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth, db: Session = Depends(get_db)):
    # querying database to check if user already exist
    user = db.query(User).filter(User.email == data.email).first()
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = User()
    user.name = data.name
    user.email = data.email
    user.password = get_hashed_password(data.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserOut(email=user.email, name=user.name, id=user.id)

@auth.post("/login", status_code=status.HTTP_201_CREATED, response_model=TokenSchema)
async def login(request: LoginSchema, db: Session = Depends(get_db)):
    """
    引数:
        request (LoginSchema): ログインリクエストを表すデータ。
        db (Session): データベースセッション。

    戻り値:
        dict: 生成されたアクセストークンとトークンタイプ。

    例外:
        HTTPException: ユーザーが見つからないか、パスワードが間違っている場合。
    """
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect email or password'
        )

    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }
