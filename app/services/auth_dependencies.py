from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from app.services.auth_services import SECRET_KEY, ALGORITHM

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials= Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if "sub" not in payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return payload
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")