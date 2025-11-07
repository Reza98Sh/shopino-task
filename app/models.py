import time

from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, Boolean, Unicode, DateTime, event, select, func

from app.database import Base
from app.base62 import Base62


class Link(Base):
    """Link model for URL shortening"""

    __tablename__ = "links"

    id = Column(Integer, primary_key=True, autoincrement=True)
    long_url = Column(Unicode(1000), index=True)
    short_code = Column(Unicode(6), unique=True, index=True, default=None)

    expire_after = Column(Integer, default=None)
    is_disabled = Column(Boolean, default=False)

    created_at = Column(DateTime(), default=func.now())
    updated_at = Column(DateTime(), default=func.now(), onupdate=func.now())


@event.listens_for(Link, "after_insert")
def generate_short_code(mapper, connection, target):
    base62 = Base62()
    # Generate a unique short code from the primary key
    code = base62.encode(target.id)
    # Update the same row with the new code
    connection.execute(
        Link.__table__.update()
            .where(Link.id == target.id)
            .values(short_code=code)
    )


class LinkManager:
    """Link model manager"""

    def __init__(self, link: Optional[Link] = None):
        self.link = link

    @property
    def expire_at_epoch(self) -> float:
        """Returns expiration epoch in seconds"""
        if self.link and self.link.expire_after and self.link.created_at:
            return self.link.created_at.timestamp() + (self.link.expire_after * 60)
        return float("inf")

    def disable(self, db: Session) -> None:
        """Disable a link"""
        if not self.link:
            raise ValueError("No link object to disable")

        self.link.is_disabled = True
        db.commit()

    def has_expired(self, db: Session) -> bool:
        """Check if link has expired"""
        if self.link and self.link.is_disabled:
            return True

        if self.link and time.time() >= self.expire_at_epoch:
            self.disable(db)
            return True

        return False

    def add(self, db: Session, long_url: str, **kwargs) -> Link:
        """Add new link to database"""

        self.link = Link(long_url=long_url, **kwargs)

        db.add(self.link)

        try:
            db.commit()
            db.refresh(self.link)
        except IntegrityError:
            db.rollback()
            raise IntegrityError(
                "Link with this URL already exists", params=None, orig=None)

        return self.link

    def get_by_code(self, db: Session, short_code: str) -> Optional[Link]:
        """Get link by short code"""
        query = select(Link).filter(Link.short_code == short_code)
        result = db.execute(query)
        self.link = result.scalars().first()
        return self.link