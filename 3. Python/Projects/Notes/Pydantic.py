from pydantic import BaseModel, Field, ConfigDict, EmailStr, HttpUrl, SecretStr, field_validator, model_validator, ValidationInfo
from datetime import datetime, UTC
from typing import Literal, Annotated
from uuid import UUID, uuid4

class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    # required
    username: Annotated[str, Field(min_length=3, max_length=20)]
    uid: UUID = Field(alias="id", default_factory=uuid4)
    age: Annotated[int, Field(ge=13, le=125)]
    email: EmailStr
    password: SecretStr

    website: HttpUrl | None = None

    # optional
    isActive: bool = False

    # optional or None
    bio: str | None = None
    verified_at: datetime | None = None

    @field_validator("username")
    @classmethod
    def validate_user(cls, v:str) -> str:
        if not v.replace("_", "").isalnum():
            raise ValueError("Username must be alphanumeric")
        return v.lower()

class BlogPost(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    content: Annotated[str, Field(min_length=10)]
    view_count: int = 0
    is_published: bool = False
    author_id: str | int

    tag: list[str] = Field(default_factory=list)
    create_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    status: Literal["draft", "published", "archived"] = "draft"

    slug: Annotated[str, Field(pattern=r"^[a-z0-9-]+$")]

user_data = {
    "id": None,
    "username": "wiggly",
    "age": 18,
    "email": "michaelvu1607@gmail.com",
    "password": "12345"
}

# model_validate_json for importing json files
user = User.model_validate(user_data)

print(user.username)
