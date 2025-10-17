# app/auth.py
from datetime import datetime, timedelta, timezone
import os

from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext

# Load .env (SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS)
load_dotenv()

# ----- Config -----
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")     # change in prod
ALGORITHM = os.getenv("ALGORITHM", "HS256")
EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", "7"))

# Use bcrypt_sha256 to avoid bcrypt's 72-byte password limit safely
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

# ----- Password hashing / verification -----
def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# ----- JWT creation -----
def create_access_token(sub: str, username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=EXPIRE_DAYS)
    payload = {"sub": sub, "username": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
