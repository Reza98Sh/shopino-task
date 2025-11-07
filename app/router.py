from typing import Optional
from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, field_validator
from app.models import LinkManager
import validators


def resolve_short(short_code: str) -> str:
    """
    Return the original long URL for the given short code.
    Raises:
        AssertionError: If link not found or disabled.
        ValueError: If link has expired.
    """
    manager = LinkManager()
    link = manager.get_by_code(short_code=short_code)
    assert link is not None, "Link not found or disabled"

    if manager.has_expired():
        raise ValueError("Link has expired")

    return link.long_url


# ---------------- Pydantic Schemas ----------------
class LinkCreate(BaseModel):
    long_url: str
    expire_after: Optional[int] = None

    @field_validator("long_url")
    def validate_long_url(cls, value: str) -> str:
        """Ensure the provided URL is valid."""
        if not validators.url(value):
            raise ValueError("Invalid URL.")
        return value


class LinkResponse(BaseModel):
    id: Optional[int]
    long_url: str
    short_code: str
    short_url: str
    created_at: Optional[str]
    expire_after: Optional[int]

    class Config:
        from_attributes = True


# ---------------- FastAPI Router ----------------
router = APIRouter()
link_manager = LinkManager()


@router.post(
    "/long-url",
    response_model=LinkResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    summary="Create a short URL",
)
async def create_short_url(link_data: LinkCreate, request: Request) -> LinkResponse:
    """ Creates a short version of the provided long URL and returns its details."""
    try:
        data = link_data.model_dump()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    long_url: str = data.pop("long_url")
    link = link_manager.add(long_url, **data)
    # link = link_manager.get(long_url)

    # if link is None:
    #     try:
    #         link = link_manager.add(long_url, **data)
    #     except Exception as e:
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
    #         )

    return link


@router.get(
    "/{code}",
    response_class=RedirectResponse,
    status_code=status.HTTP_301_MOVED_PERMANENTLY,
    summary="Redirect to the original URL",
)
async def resolve_url(code: str, request: Request) -> RedirectResponse:
    """Resolve the short URL and redirect to the original long URL."""
    try:
        long_url: str = resolve_short(code)
        return RedirectResponse(url=long_url, status_code=status.HTTP_301_MOVED_PERMANENTLY)

    except ValueError:
        raise HTTPException(status_code=404, detail="Link has expired")

    except (Exception, AssertionError):
        raise HTTPException(
            status_code=404, detail="URL not found or disabled"
        )
