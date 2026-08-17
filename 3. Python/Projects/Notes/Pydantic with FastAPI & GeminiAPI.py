from pydantic import BaseModel, Field, ValidationError
from datetime import datetime, UTC
from typing import Literal, Annotated

class User(BaseModel):
    # required
    username: Annotated[str, Field(min_length=3, max_length=20)]
    uid: Annotated[int, Field(gt=0)]
    age: Annotated[int, Field(ge=13, le=125)]

    # optional
    isActive: bool = False

    # optional or None
    bio: str | None = None
    verified_at: datetime | None = None

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

