from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, SecurityScopes
from shared.infrastructure import ErrorResponse
from fastapi import Depends, status, Request
from jose import jws, JWSError, ExpiredSignatureError
import uuid
import json


bearer_schema = HTTPBearer()
uid = str(uuid.uuid4())


async def authentication(request: Request, token: HTTPAuthorizationCredentials = Depends(bearer_schema)):
    try:
        unauthorized_exception = ErrorResponse(
            message="Usuario no autorizado",
            status_code=status.HTTP_401_UNAUTHORIZED,
            transaction_id=uid,
            details=["Error al obtener la información del usuario"]
        )
        secret_key = request.headers.get("secret_key", "")
        payload = json.loads(jws.verify(token.credentials, secret_key, "HS256"))
        user = payload["sub"]
        if not user.get("rol", []):
            raise unauthorized_exception
        
        return user

    except JWSError:
        unauthorized_exception.meta["details"] = ["Token inválido o secret key incorrecta"]
        raise unauthorized_exception
    except ExpiredSignatureError:
        unauthorized_exception.meta["details"] = ["El token ha expirado"]
        raise unauthorized_exception
    except Exception:
        unauthorized_exception.meta["details"] = ["El payload es inválido o no es posible decodificar"]
        raise unauthorized_exception


async def authorization(security_scopes: SecurityScopes, user: dict = Depends(authentication)):
    not_enough_permissions_exception = ErrorResponse(
        message="Usuario no autorizado",
        transaction_id=uid,
        status_code=status.HTTP_403_FORBIDDEN,
        details=["El usuario no tiene el rol permitido"]
    )
    roles = user.get("rol", [])
    for scope in security_scopes.scopes:
        if scope not in roles:
            raise not_enough_permissions_exception
    
    return user