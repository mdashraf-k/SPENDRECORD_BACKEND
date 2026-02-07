from databases.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

class Spend(Base):
    __tablename__ = "spends"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    description = Column(String(150))
    amount = Column(Integer, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False, index=True)

    group = relationship("Group")
    user = relationship("User")