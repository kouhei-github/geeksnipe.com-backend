from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.index import User
from schemas.index import UserSchema, ShowUserSchema, TokenDataSchema
from config.index import get_db
from services.hashing import Hash
from midlewares.index import get_current_bearer_token

user = APIRouter(
    prefix="/api/user",
    tags=["Users"]
)

@user.get("/", response_model= List[ShowUserSchema])
async def read_all_users(
    db: Session = Depends(get_db),
    get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token)
):
    """データベースから全てのユーザーを読み込む

    Args:
        db (Session):  使用するデータベースセッション

    Returns:
        List[ShowUserSchema]: 全ユーザのリスト

    Raises:
        HTTPException: データベースからユーザーを取得する際にエラーが発生した場合

    """

    user = db.query(User).filter(User.id == get_bearer_token.user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED,
            detail=f'Authorization is required'
        )

    users = db.query(User).all()
    return users

@user.get("/{id}", response_model=ShowUserSchema)
async def show_user(
    id: int,
    db: Session = Depends(get_db),
    get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token)
):
    """
    ユーザーを表示

    データベースから特定のユーザーを取得する

    Args:
        id (int):  取得するユーザーのID
        db (Session): データベースセッション
        get_bearer_token (TokenDataSchema): The current bearer token.

    Returns:
        ShowUserSchema: 取得したユーザー

    Raises:
        HTTPException:  指定した ID のユーザがデータベースに存在しない場合
    """
    user = db.query(User).filter(User.id == get_bearer_token.user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED,
            detail=f'Authorization is required'
        )

    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with the id {id} is not available'
        )
    return user

@user.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_user(
    id: int,
    request: UserSchema,
    db: Session = Depends(get_db),
    get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token)
):
    """
    Args:
        id (int): The ID of the user to be updated.
        request (UserSchema): The updated user data.
        db (Session): The SQLAlchemy session.
        get_bearer_token (TokenDataSchema): The current bearer token.

    Returns:
        dict: A dictionary with the message "update completed"

    Raises:
        HTTPException: If the user with the specified ID is not found in the database.

    """
    user = db.query(User).filter(User.id == get_bearer_token.user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED,
            detail=f'Authorization is required'
        )

    user = db.query(User).filter(User.id == id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with the id {id} is not available'
        )
    hashing = Hash()
    request.password = hashing.bcript(request.password)
    user.update(request.dict())
    db.commit()
    return {"msg": "update completed"}

@user.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: int,
    db: Session = Depends(get_db),
    get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token)
):
    """
    Args:
        id (int): The ID of the user to be deleted.
        db (Session): The database session.
        get_bearer_token (TokenDataSchema): The current bearer token.

    Returns:
        dict: A dictionary with the message "delete completed".

    Raises:
        HTTPException: If a user with the specified ID is not found.

    """
    user = db.query(User).filter(User.id == get_bearer_token.user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED,
            detail=f'Authorization is required'
        )

    user = db.query(User).filter(User.id == id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with the id {id} is not available'
        )
    user.delete(synchronize_session=False)
    db.commit()
    return {"msg": "delete completed"}

