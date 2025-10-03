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

class RoleEnum(enum.Enum):
    CREATOR = "creator"
    ADMIN = "admin"
    USER = "user"

ROLE_PERMISSIONS = {
    "admin": ["create_campaign", "delete_user", "view_reports", "edit_meme"],
    "creator": ["upload_meme", "edit_meme"],
    "user": ["vote_meme"],
}
