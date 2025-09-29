from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Placeholder: en el proyecto general este endpoint existirá
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # TODO: integrar con servicio de autenticación central
    if not token or token != "fake-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o no provisto",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"user": "demo"}  # Simulación temporal