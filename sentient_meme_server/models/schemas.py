from pydantic import BaseModel

from types_1 import CategoryEnum, RarityEnum

# class Badge(Base):
#     __tablename__ = "badges"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     description = Column(String, nullable=False)
#     rarity = Column(Enum(RarityEnum), nullable=False)
#     category = Column(Enum(CategoryEnum), nullable=False)
#     requirements = Column(String, nullable=False)
#     badge_image = Column(String, nullable=False)

#     created_at = Column(DateTime, default=datetime.now)
#     updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

class BadgeSchema(BaseModel):
    id: int
    name: str
    description: str
    rarity: RarityEnum
    category: CategoryEnum
    requirements: str
    badge_image: str

    model_config = {
        "from_attributes": True
    }

class BadgeCreate(BaseModel):
    name: str
    description: str
    rarity: RarityEnum
    category: CategoryEnum
    requirements: str
    badge_image: str
