import uuid

from sqlalchemy import Column, Float, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all score models.
    """


class Score(Base):
    """
    SQLAlchemy model for the score table.
    """

    __tablename__ = "scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    risk_score: Column[float] = Column(Float, nullable=False)
    risk_label = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)

    def __repr__(self):
        return f"<Score {self.risk_label} ({self.risk_score})>"
