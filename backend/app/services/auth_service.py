from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.models.user import User
from app.models.freelancer import FreelancerProfile
from app.models.client import ClientProfile
from app.schemas.auth import UserCreate
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    def create_token(self, user_id: int) -> str:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return jwt.encode(
            {"sub": str(user_id), "exp": expire},
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

    async def register(self, user_data: UserCreate, db: Session) -> User:
        # Kontrollo nëse ekziston
        existing = db.query(User).filter(
            (User.email == user_data.email) |
            (User.username == user_data.username)
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email ose username ekziston tashmë"
            )

        # Krijo userin
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=self.hash_password(user_data.password),
            role=user_data.role
        )
        db.add(user)
        db.flush()

        # Krijo profilin sipas rolit
        if user_data.role == "freelancer":
            profile = FreelancerProfile(user_id=user.id)
            db.add(profile)
        elif user_data.role == "client":
            profile = ClientProfile(user_id=user.id)
            db.add(profile)

        db.commit()
        db.refresh(user)
        return user

    async def login(self, username: str, password: str, db: Session) -> dict:
        user = db.query(User).filter(User.username == username).first()
        if not user or not self.verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username ose password i gabuar"
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Llogaria është e çaktivizuar"
            )
        token = self.create_token(user.id)
        return {"access_token": token, "token_type": "bearer"}

    async def refresh_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            user_id = int(payload.get("sub"))
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token i pavlefshëm"
            )
        new_token = self.create_token(user_id)
        return {"access_token": new_token, "token_type": "bearer"}