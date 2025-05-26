from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import User, CreateUser, LoginUser, UserWithToken
from app.cruds import user as crud_user
from app.db.database import get_db
from datetime import timedelta
from jose import jwt, JWTError
from app.core.security import verify_password, ouauth2scheme, create_access_token, SECRET_KEY, ALGORITHM
from app.services.scipher import scipher
from app.schemas.scipher import ToEncode, Result


router = APIRouter()


@router.post("/sign-up", response_model=UserWithToken)
def sign_up(user: CreateUser, db: Session = Depends(get_db)) -> UserWithToken:
    db_user = crud_user.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='email уже зарегестрирован'
        )

    user = crud_user.create_user(db=db, user=user)
    token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=15)
    )

    return UserWithToken(
        id=user.id,
        email=user.email,
        token=token
    )


@router.post("/login", response_model=UserWithToken)
def login(user: LoginUser, db: Session = Depends(get_db)) -> UserWithToken:
    db_user = crud_user.get_user_by_email(db, email=user.email)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не зарегестрирован"
        )

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль"
        )

    token = create_access_token(
        data={"sub": db_user.id},
        expires_delta=timedelta(minutes=15)
    )

    return UserWithToken(
        id=db_user.id,
        email=db_user.email,
        token=token
    )


@router.get("/users/me", response_model=User)
def get_user(db: Session = Depends(get_db), token: str = Depends(ouauth2scheme)) -> User:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен не валидирован"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="токен не валидирован"
        )

    user = crud_user.get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return user


@router.post("/encode", response_model=Result)
def encode(toencode: ToEncode) -> Result:
    return scipher(toencode)
