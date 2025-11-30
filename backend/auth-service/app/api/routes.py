from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
import httpx

from app.api.deps import get_current_user
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/me")
def me(user=Depends(get_current_user)):
    return user

@router.post("/verify")
def verify(user=Depends(get_current_user)):
    return {
        "uid": user.get("uid"),
        "email": user.get("email"),
        "claims": user,
    }

class RegisterBody(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

@router.post("/dev/register")
async def dev_register(body: RegisterBody):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={settings.FIREBASE_WEB_API_KEY}"
    payload = {
        "email": body.email,
        "password": body.password,
        "returnSecureToken": True,
    }

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(url, json=payload)

    data = r.json()
    if r.status_code != 200:
        msg = (data.get("error") or {}).get("message", "REGISTER_FAILED")
        raise HTTPException(status_code=400, detail=msg)

    return {
        "uid": data.get("localId"),
        "email": data.get("email"),
        "idToken": data.get("idToken"),
        "refreshToken": data.get("refreshToken"),
        "expiresIn": data.get("expiresIn"),
    }


class LoginBody(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

@router.post("/dev/login")
async def dev_login(body: LoginBody):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={settings.FIREBASE_WEB_API_KEY}"
    payload = {
        "email": body.email,
        "password": body.password,
        "returnSecureToken": True,
    }

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(url, json=payload)

    data = r.json()
    if r.status_code != 200:
        msg = (data.get("error") or {}).get("message", "LOGIN_FAILED")
        raise HTTPException(status_code=400, detail=msg)

    return {
        "uid": data.get("localId"),
        "email": data.get("email"),
        "idToken": data.get("idToken"),
        "refreshToken": data.get("refreshToken"),
        "expiresIn": data.get("expiresIn"),
    }
