from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from typing import Optional, List
from datetime import date, datetime, timedelta
from collections import Counter

from app.database import get_db
from app.dependencies import get_current_user
from app.models.mood import Mood
from app.models.user import User
from app.schemas.mood import MoodCreate, MoodResponse, MoodSummary, MoodListResponse

router = APIRouter()

@router.post("/add", response_model=MoodResponse, status_code=status.HTTP_201_CREATED)
async def add_mood(
    mood_data: MoodCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new mood entry for the authenticated user.
    
    - **date**: Date for the mood entry (YYYY-MM-DD format)
    - **moodLevel**: Mood level from 1-5 (1=very bad, 5=excellent)
    - **tags**: Optional list of tags (max 10, each max 20 chars)
    - **notes**: Optional notes (max 1000 chars)
    
    Returns 201 if created successfully, 400 if entry already exists for that date.
    """
    # Check if entry already exists for this user and date
    existing_mood = db.query(Mood).filter(
        and_(Mood.user_id == current_user.id, Mood.date == mood_data.date)
    ).first()
    
    if existing_mood:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Mood entry already exists for this date"}
        )
    
    # Convert tags list to comma-separated string
    tags_string = None
    if mood_data.tags:
        tags_string = ",".join(mood_data.tags)
    
    # Create new mood entry
    new_mood = Mood(
        user_id=current_user.id,
        date=mood_data.date,
        mood_level=mood_data.moodLevel,
        tags=tags_string,
        notes=mood_data.notes
    )
    
    db.add(new_mood)
    db.commit()
    db.refresh(new_mood)
    
    # Convert tags back to list for response
    tags_list = None
    if new_mood.tags:
        tags_list = [tag.strip() for tag in new_mood.tags.split(',') if tag.strip()]
    
    return MoodResponse(
        id=new_mood.id,
        user_id=new_mood.user_id,
        date=new_mood.date,
        mood_level=new_mood.mood_level,
        tags=tags_list,
        notes=new_mood.notes
    )

@router.get("/all", response_model=MoodListResponse)
async def get_all_moods(
    from_date: Optional[date] = Query(None, alias="from", description="Start date filter"),
    to_date: Optional[date] = Query(None, alias="to", description="End date filter"),
    limit: int = Query(100, ge=1, le=1000, description="Number of entries to return"),
    offset: int = Query(0, ge=0, description="Number of entries to skip"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all mood entries for the authenticated user.
    
    - **from**: Optional start date filter (YYYY-MM-DD)
    - **to**: Optional end date filter (YYYY-MM-DD)
    - **limit**: Number of entries to return (1-1000, default 100)
    - **offset**: Number of entries to skip for pagination (default 0)
    
    Returns paginated list of mood entries ordered by date ascending.
    """
    query = db.query(Mood).filter(Mood.user_id == current_user.id)
    
    # Apply date filters
    if from_date:
        query = query.filter(Mood.date >= from_date)
    if to_date:
        query = query.filter(Mood.date <= to_date)
    
    # Get total count
    total = query.count()
    
    # Apply pagination and ordering
    moods = query.order_by(Mood.date.asc()).offset(offset).limit(limit).all()
    
    # Convert to response format
    mood_responses = []
    for mood in moods:
        tags_list = None
        if mood.tags:
            tags_list = [tag.strip() for tag in mood.tags.split(',') if tag.strip()]
        
        mood_responses.append(MoodResponse(
            id=mood.id,
            user_id=mood.user_id,
            date=mood.date,
            mood_level=mood.mood_level,
            tags=tags_list,
            notes=mood.notes
        ))
    
    return MoodListResponse(
        moods=mood_responses,
        total=total,
        limit=limit,
        offset=offset
    )

@router.get("/summary", response_model=MoodSummary)
async def get_mood_summary(
    range_type: Optional[str] = Query(None, alias="range", description="Time range: 'week' or 'month'"),
    from_date: Optional[date] = Query(None, alias="from", description="Custom start date"),
    to_date: Optional[date] = Query(None, alias="to", description="Custom end date"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get mood statistics and summary for the authenticated user.
    
    - **range**: Time range - 'week' (last 7 days) or 'month' (last 30 days)
    - **from**: Custom start date (overrides range if provided)
    - **to**: Custom end date (overrides range if provided)
    
    Returns summary with total entries, average mood, daily breakdown, top tags, and trend.
    """
    # Determine date range
    end_date = date.today()
    
    if from_date and to_date:
        # Custom date range
        start_date = from_date
        end_date = to_date
    elif range_type == "week":
        start_date = end_date - timedelta(days=6)
    elif range_type == "month":
        start_date = end_date - timedelta(days=29)
    else:
        # Default to month
        start_date = end_date - timedelta(days=29)
    
    # Get mood entries in the date range
    moods = db.query(Mood).filter(
        and_(
            Mood.user_id == current_user.id,
            Mood.date >= start_date,
            Mood.date <= end_date
        )
    ).order_by(Mood.date.asc()).all()
    
    if not moods:
        return MoodSummary(
            total=0,
            average=0.0,
            by_day=[],
            top_tags=[],
            trend="flat"
        )
    
    # Calculate statistics
    total = len(moods)
    average = sum(mood.mood_level for mood in moods) / total
    
    # Create daily breakdown
    by_day = [
        {"date": mood.date.isoformat(), "mood": mood.mood_level}
        for mood in moods
    ]
    
    # Calculate top tags
    all_tags = []
    for mood in moods:
        if mood.tags:
            all_tags.extend([tag.strip() for tag in mood.tags.split(',') if tag.strip()])
    
    # Get top 5 tags by frequency
    tag_counts = Counter(all_tags)
    top_tags = [tag for tag, count in tag_counts.most_common(5)]
    
    # Calculate trend
    trend = "flat"
    if len(moods) >= 14:  # Need at least 2 weeks of data
        # Split into two equal periods
        mid_point = len(moods) // 2
        first_half = moods[:mid_point]
        second_half = moods[mid_point:]
        
        first_avg = sum(mood.mood_level for mood in first_half) / len(first_half)
        second_avg = sum(mood.mood_level for mood in second_half) / len(second_half)
        
        diff = second_avg - first_avg
        if abs(diff) <= 0.1:
            trend = "flat"
        elif diff > 0.1:
            trend = "up"
        else:
            trend = "down"
    
    return MoodSummary(
        total=total,
        average=round(average, 2),
        by_day=by_day,
        top_tags=top_tags,
        trend=trend
    )

@router.get("/{mood_date}", response_model=MoodResponse)
async def get_mood_by_date(
    mood_date: date,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get mood entry for a specific date for the authenticated user.
    
    - **mood_date**: Date to retrieve mood for (YYYY-MM-DD format)
    
    Returns 404 if no entry exists for that date.
    """
    mood = db.query(Mood).filter(
        and_(Mood.user_id == current_user.id, Mood.date == mood_date)
    ).first()
    
    if not mood:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "No mood entry found for this date"}
        )
    
    # Convert tags back to list for response
    tags_list = None
    if mood.tags:
        tags_list = [tag.strip() for tag in mood.tags.split(',') if tag.strip()]
    
    return MoodResponse(
        id=mood.id,
        user_id=mood.user_id,
        date=mood.date,
        mood_level=mood.mood_level,
        tags=tags_list,
        notes=mood.notes
    )
