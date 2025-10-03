import enum

class RarityEnum(enum.Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

class CategoryEnum(enum.Enum):
    ACHIEVEMENT = "achievement"
    PERFORMANCE = "performance"
    CREATIVITY = "creativity"
    THEME = "theme"
    SOCIAL = "social"
    PARTICIPATION = "participation"
    SPECIAL = "special"