from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

router = APIRouter()

# GET /profile/get
@router.get("/get")
def get_profile(db: Session = Depends(get_db)):
    return {
        "theme": "light",
        "notification_style": "default",
        "reminder_frequency": "daily",
        "privacy_toggle": "public"
    }

# PUT /profile/update
@router.put("/update")
def update_profile(
    db: Session = Depends(get_db),
    theme: str = "dark",
    notification_style: str = "minimal",
    reminder_frequency: str = "weekly",
    privacy_toggle: str = "private"
):
    return {
        "success": True,
        "message": "Profile updated successfully",
        "data": {
            "theme": theme,
            "notification_style": notification_style,
            "reminder_frequency": reminder_frequency,
            "privacy_toggle": privacy_toggle
        }
    }

# GET /profile/export
@router.get("/export")
def export_profile(db: Session = Depends(get_db)):
    return {
        "user_id": "test-user",
        "profile": {
            "theme": "dark",
            "notification_style": "minimal",
            "reminder_frequency": "weekly",
            "privacy_toggle": "private"
        }
    }
