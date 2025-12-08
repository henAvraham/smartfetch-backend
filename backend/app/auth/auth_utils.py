from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User


SECRET_KEY = "supersecretkey_change_me" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



def hash_password(password: str) -> str:
    """המרת סיסמה לטקסט מוצפן לשמירה בדאטאבייס."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """בדיקת התאמה בין סיסמה רגילה לבין הגרסה המוצפנת שלה."""
    return pwd_context.verify(plain_password, hashed_password)



def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    מחפש משתמש לפי username ובודק שהסיסמה נכונה.
    מחזיר את המשתמש אם הכול תקין, אחרת None.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None

   
    if not verify_password(password, user.password):
        return None

    return user



def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    יצירת JWT עם תאריך תפוגה.
    מקובל לשים ב-data משהו כמו {"sub": "<user_id כטקסט>"}.
    """
    to_encode = data.copy()

    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    מפענח את ה-JWT, מוציא ממנו את ה-user_id (sub),
    ומחזיר את אובייקט ה-User המתאים.
    אם משהו לא תקין -> 401.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception

        
        try:
            user_id = int(sub)
        except (TypeError, ValueError):
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user



