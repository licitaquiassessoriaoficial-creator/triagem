"""
Serviço de Autenticação
Gerencia tokens JWT e autenticação de usuários
"""

import hashlib
import os
from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import HTTPException, status


class AuthService:
    """Serviço de autenticação JWT"""

    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ):
        """Criar token JWT"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.secret_key, algorithm=self.algorithm
        )
        return encoded_jwt

    async def verify_token(self, token: str):
        """Verificar token JWT"""
        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return username
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        """Verificar senha usando hash simples"""
        plain_hash = hashlib.sha256(plain_password.encode()).hexdigest()
        return plain_hash == hashed_password

    def get_password_hash(self, password: str) -> str:
        """Hash da senha usando SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
