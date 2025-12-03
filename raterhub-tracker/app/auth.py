from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from .db_models import User

# -------------------------------------------------------------------
# JWT / crypto configuration
# -------------------------------------------------------------------

# ⚠️ In production, load this from an environment variable.
# Example to generate one:
#   python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY = "CHANGE_ME_TO_A_LONG_RANDOM_HEX_STRING"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Use pbkdf2_sha256 to avoid bcrypt backend quirks & 72-byte limits
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


# -------------------------------------------------------------------
# Password helpers
# -------------------------------------------------------------------

def verify_password(plain_password: str, password_hash: str) -> bool:
    """
    Verify a plain-text password against a stored hash.
    """
    return pwd_context.verify(plain_password, password_hash)


def get_password_hash(password: str) -> str:
    """
    Hash a plain-text password for storage.
    """
    return pwd_context.hash(password)


# -------------------------------------------------------------------
# JWT helpers
# -------------------------------------------------------------------

def create_access_token(
    *,
    user: User,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a signed JWT for the given user.

    Payload includes:
      - sub: user.id
      - email: user.email
      - exp: expiration timestamp
    """
    to_encode: Dict[str, Any] = {
        "sub": str(user.id),
        "email": user.email,
    }

    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT.

    Returns the payload dict on success, or None on failure.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
