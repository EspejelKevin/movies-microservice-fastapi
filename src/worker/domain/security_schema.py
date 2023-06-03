from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, SecurityScopes
from shared.infrastructure import ErrorResponse
from fastapi import Depends, status
import uuid


bearer_schema = HTTPBearer()
uid = str(uuid.uuid4())


async def authentication(token: HTTPAuthorizationCredentials = Depends(bearer_schema)):
    try:
        unauthorized_exception = ErrorResponse(
            message="Usuario no autorizado",
            status_code=status.HTTP_401_UNAUTHORIZED,
            transaction_id=uid
        )
        
        payload = {}
        
        return payload

    except Exception as e:
        unauthorized_exception.meta["details"] = e
        raise unauthorized_exception


async def authorization(security_scopes: SecurityScopes, user: dict = Depends(authentication)):
    not_enough_permissions_exception = ErrorResponse(
        message="Usuario no autorizado",
        transaction_id=uid,
        status_code=status.HTTP_403_FORBIDDEN,
        details=["El usuario no tiene el rol permitido"]
    )
    roles = []
    for scope in security_scopes.scopes:
        if scope not in roles:
            raise not_enough_permissions_exception
    
    return user