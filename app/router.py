
from typing import Optional
from datetime import datetime
from app.models import LinkManager
from sqlalchemy.orm import Session
from validators import url as valid_url
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, field_validator
from fastapi import APIRouter, HTTPException, status, Request, Depends

from app.database import get_db


def resolve_short(short_code: str, db: Session) -> str:
    """Return the original long URL for the given short code."""

    manager = LinkManager()
    link = manager.get_by_code(db=db, short_code=short_code)
    assert link is not None, "Link not found or disabled"

    if manager.has_expired(db=db):
        raise ValueError("Link has expired")

    return link.long_url


# ---------------- Pydantic Schemas ----------------
class LinkCreate(BaseModel):
    long_url: str
    expire_after: Optional[int] = None

    @field_validator("long_url")
    def validate_long_url(cls, value: str) -> str:
        """Ensure the provided URL is valid."""
        if not valid_url(value):
            raise ValueError("Invalid URL.")
        return value


class LinkResponse(BaseModel):
    id: Optional[int]
    long_url: str
    short_code: str
    short_url: str
    created_at: Optional[datetime]
    expire_after: Optional[int]

    class Config:
        from_attributes = True


# ---------------- FastAPI Router ----------------
router = APIRouter()


@router.post(
    "/api/long-url",
    response_model=LinkResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
async def create_short_url(
    link_data: LinkCreate, request: Request, db: Session = Depends(get_db)
) -> LinkResponse:
    """Creates a short version of the provided long URL and returns its details."""
    try:
        data = link_data.model_dump()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    link_manager = LinkManager()
    long_url: str = data.pop("long_url")
    link = link_manager.add(db, long_url)
    short_url = f"{str(request.base_url)}{link.short_code}"

    return LinkResponse(
        id=link.id,
        long_url=link.long_url,
        short_code=link.short_code,
        short_url=short_url,
        created_at=link.created_at,
        expire_after=link.expire_after,
    )


@router.get(
    "/{code}",
    response_class=RedirectResponse,
    status_code=status.HTTP_301_MOVED_PERMANENTLY,
)
async def resolve_url(
    code: str, request: Request, db: Session = Depends(get_db)
) -> RedirectResponse:
    """Resolve the short URL and redirect to the original long URL."""
    try:
        long_url: str = resolve_short(code, db)
        return RedirectResponse(
            url=long_url, status_code=status.HTTP_301_MOVED_PERMANENTLY
        )

    except ValueError:
        raise HTTPException(status_code=404, detail="Link has expired")

    except (Exception, AssertionError):
        raise HTTPException(status_code=404, detail="URL not found or disabled")
