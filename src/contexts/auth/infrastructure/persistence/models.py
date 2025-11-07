from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from src.contexts.auth.domain.aggregates import ApiKey, User
from src.contexts.shared.infrastructure.persistence.base import SQLAlchemyBaseModel


class UserModel(SQLAlchemyBaseModel):
    __tablename__ = "users"

    user_id = Column(String(36), primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    api_keys = relationship(
        "ApiKeyModel",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @staticmethod
    def from_domain(user: User) -> "UserModel":
        return UserModel(
            user_id=str(user.user_id),
            username=user.username,
            email=user.email,
            password=user.password,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def to_domain(self) -> User:
        return User(
            user_id=self.user_id,
            username=self.username,
            email=self.email,
            password=self.password,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
            api_keys=[api_key.to_domain() for api_key in self.api_keys],
        )


class ApiKeyModel(SQLAlchemyBaseModel):
    __tablename__ = "api_keys"

    api_key_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    api_key = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False)

    user = relationship("UserModel", back_populates="api_keys")

    @staticmethod
    def from_domain(api_key: ApiKey) -> "ApiKeyModel":
        return ApiKeyModel(
            api_key_id=str(api_key.api_key_id),
            user_id=str(api_key.user_id),
            api_key=api_key.api_key,
            is_active=api_key.is_active,
            created_at=api_key.created_at,
            updated_at=api_key.updated_at,
        )

    def to_domain(self) -> ApiKey:
        return ApiKey(
            api_key_id=self.api_key_id,
            user_id=self.user_id,
            api_key=self.api_key,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
