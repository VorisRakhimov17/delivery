import secrets

from fastapi import Depends, FastAPI, HTTPException, APIRouter, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from schemas import SignupModel, LoginModel
from database import session, engine
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT

auth_router = APIRouter(
    prefix="/auth",
)

session = session(bind=engine)


@auth_router.get("/")
async def signup(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token kiritilmadi")
    return {"message": "Bu auth route signup sahifasi"}


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: SignupModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Bu email orqali avval ro'yxatdan o'tgan")

    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Bu username orqali avval ro'yxatdan o'tgan")

    new_user = User(
        email=user.email,
        username=user.username,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    session.add(new_user)
    session.commit()
    response_model = {
        "message": "success",
        "code": 201,
        "data": {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'is_staff': new_user.is_staff,
            'is_active': new_user.is_active,
        }
    }
    return response_model

@auth_router.post("/login", status_code=200)
async def login(user: LoginModel,  Authorize: AuthJWT=Depends()):
    db_user = session.query(User).filter(User.username == user.username).first()
    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=user.username)
        refresh_token = Authorize.create_refresh_token(subject=user.username)

        token = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        response = {
            "success": True,
            "code": 200,
            "message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi",
            "data": token
        }

        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parol yoki usernmae xato")