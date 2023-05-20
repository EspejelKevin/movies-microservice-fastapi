from pydantic import BaseModel, validator, Field
from fastapi import Query
from datetime import date
from typing import Optional


class MovieModelIn(BaseModel):
    name: str
    description: str
    original_language: str
    dubbing: list
    has_subtitles: bool
    gender: str
    release_date: date
    rating: int
    length: int

    @validator(
        "name",
        "description",
        "original_language",
        "gender",
        pre=True
    )
    def must_be_str(cls, v):
        if not isinstance(v, str):
            raise ValueError("must be str")
        return v

    @validator("has_subtitles", pre=True)
    def must_be_bool(cls, v):
        if not isinstance(v, bool):
            raise ValueError("must be bool")
        return v

    @validator("dubbing", pre=True)
    def verify_len(cls, v):
        if not v or not isinstance(v, list):
            raise ValueError("must be a list with dubbing")
        return v

    @validator("rating", pre=True)
    def validate_range(cls, v):
        if v < 0 or v > 5:
            raise ValueError("must be in the range 0 - 5")
        return v

    @validator("length", pre=True)
    def validate_length_in_minutes(cls, v):
        if v < 90:
            raise ValueError("must be in minutes. Minimum value is 90 min")
        return v


class MovieModel(MovieModelIn):
    id_movie: int
    url: str = ""


class QueryFilterModel(BaseModel):
    rating: Optional[int] = Field(Query(default=None, title="Rating", description="Rating of the movies", example=5))
    gender: Optional[str] = Field(Query(default=None, title="Gender", description="Gender of the movies", example="Accion"))
    release_date_desc: Optional[bool] = Field(Query(
        default=False, 
        title="Release date descending", 
        description="Filter up or down",
        example=True
    ))

    @validator("rating", pre=True)
    def validate_range(cls, v):
        if v and v < 0 or v > 5:
            raise ValueError("must be in the range 0 - 5")
        return v

    @validator("gender", pre=True)
    def must_be_str(cls, v):
        if v and not isinstance(v, str):
            raise ValueError("must be str")
        return v

    @validator("release_date_desc", pre=True)
    def must_be_bool(cls, v):
        if v and not isinstance(v, bool):
            raise ValueError("must be bool")
        return v
