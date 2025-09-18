import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all session models.
    """


class Session(Base):
    """
    SQLAlchemy model for the session table.
    """

    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    session_id = Column(Text, nullable=False)
    external_user_id = Column(Text, nullable=False)
    device_fingerprint = Column(Text, nullable=False)
    ip_address = Column(Text, nullable=False)
    user_agent = Column(Text, nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.current_timestamp)  # type: ignore
    ended_at = Column(DateTime(timezone=True), nullable=True)
    event_count = Column(Integer, default=0)
    score_id = Column(Integer, nullable=True)
    # country = Column(Text, nullable=True)
    # city = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Session {self.session_id}>"

    def __str__(self):
        return str(self.session_id)
