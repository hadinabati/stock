import secrets
from typing import Optional, List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from pydantic import BaseModel

from base import checking
from base.so_base import ObjectId
from database.mongodb import User_collection
from schema.user_schema import Credentials
from schema.user_schema import user_show


# ----------------    end  importing ------------------------


async def basic_authenticate(form_data: OAuth2PasswordRequestForm = Depends()):
    credentials = Credentials(
        username=form_data.username,
        password=form_data.password
    )
    user = User_collection.find_one(
        {'username': credentials.username}
    )
    if user:
        if checking.unhashing(user.get('passwords')) == credentials.password:
            return user_show.parse_obj({**user, "id": user.get("_id")})
        else:
            raise HTTPException(status_code=200, detail={
                'is_logged': False,
                'passwords_wrong': True
            })
    else:
        raise HTTPException(status_code=404, detail={
            'is_logged': False
        })


class TokenData(BaseModel):
    id: ObjectId
    username: str
    role: Optional[List[str]]


class Token(BaseModel):
    access_token: Optional[str]
    refresh_token: Optional[str]
    token_type: str
    is_new_user: Optional[bool]
    is_loggin: bool = True


def create_access_token(
        data: dict,
) -> str:
    to_encode = data.copy()
    secrect_key = secrets.token_hex()
    encoded_jwt = jwt.encode(to_encode, str(secrect_key), algorithm='HS256')
    return encoded_jwt


def decode_access_token(
        token: str,

):
    login_credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=token,
        headers={"WWW-Authenticate": "Bearer"},
    )
    refresh_credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Access token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(str(token), key=secrets.token_hex(), options={"verify_signature": False})
    except ExpiredSignatureError:
        raise refresh_credentials_exception
    except JWTError:
        raise login_credentials_exception

    return TokenData(
        id=payload.get("sub"),
        username=payload.get("username"),
        role=payload.get("scope")
    )


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/login')


def get_current_user(token: str = Depends(oauth2_schema)):
    token_data = decode_access_token(token=token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if (token_data.username or token_data.id) is None:
        raise credentials_exception
    data = token_data.dict()
    return user_show.parse_obj({**data})


# در انتها باید تغییر کند به صورتی که نقش ها را بتوان در مدیریت به افراد الحاق کرد و نقش های ثابتی برای ادمین و کاربران وجود نداشته باشد
def permissions(permissions_list: List[str]):
    async def user_permission_checker(user: user_show = Depends(get_current_user)):
        check = False

        if len(permissions_list) == 1 and permissions_list[0] == 'authenticated':
            check = True
        else:
            for item in permissions_list:
                if item != 'authenticated' and item in user.role:
                    check = True
                    break

        if "authenticated" in permissions_list and "authenticated" not in user.role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="login",
            )

        elif check:
            pass
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='you dont have access to this point'
            )
        return user

    return user_permission_checker
