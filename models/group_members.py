from databases.database import Base
from sqlalchemy import Integer, Column, ForeignKey, String, DateTime, Boolean, func, UniqueConstraint
from sqlalchemy.orm import relationship


class GroupMembers(Base):
    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    role = Column(String, default="member", nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


    group = relationship("Group")
    user = relationship("User")

    # 👇 Prevents duplicate rows for the same user in the same group
    __table_args__ = (
        UniqueConstraint('group_id', 'user_id', name='_group_user_uc'),
    )