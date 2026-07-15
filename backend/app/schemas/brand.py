from pydantic import BaseModel, Field, field_validator


class BrandCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    slug: str = Field(..., min_length=2, max_length=255)
    market: str = Field(..., min_length=2, max_length=255)
    description: str | None = None
    status: str = Field(default="proposed")

    @field_validator("slug")
    @classmethod
    def normalize_slug(cls, value: str) -> str:
        slug = value.strip().lower().replace(" ", "-")
        if not slug:
            raise ValueError("Slug is required.")
        return slug


class BrandResponse(BaseModel):
    id: int
    name: str
    slug: str
    market: str
    description: str | None
    status: str

    class Config:
        from_attributes = True

