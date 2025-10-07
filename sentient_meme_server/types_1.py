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
    "admin": ["create_campaign", "delete_user", "edit_meme", "upload_meme"],
    "creator": ["upload_meme", "edit_meme", "delete_user", "create_campaign", "delete_user", "delete_admin", "add_admin", "create_badge", "delete_badge"],
    "user": ["vote_meme", "upload_meme"],
}
