from fastapi.security import OAuth2PasswordBearer #let the system knows we want to secure our end-point.
from fastapi.param_functions import Depends
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from sqlalchemy.orm import Session
from db.database import get_db
from fastapi import HTTPException, status
from db import db_user
from db.models import DbUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token') #not create a end-point, just say this end-point will be require to recieve token for our scheme.
 
SECRET_KEY = '006c35540019ce650f09fb583f54e6c6c673ecf903a18906cfa9097c9d8872f0' #allows us to sign a token we generate 
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=1440)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)): #get_db = db session
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'}
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get('sub')
    if username is None:
      raise credentials_exception
  except JWTError:
    raise credentials_exception
  
  user = db_user.get_user_by_username(db, username)

  if user is None:
    raise credentials_exception
  
  return user 