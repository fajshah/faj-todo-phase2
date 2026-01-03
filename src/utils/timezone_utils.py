from datetime import datetime, date, time
from typing import Optional
import zoneinfo  # Available in Python 3.9+, fallback to pytz for older versions

def convert_to_user_timezone(dt: datetime, user_timezone: str = "UTC") -> datetime:
    """
    Convert a datetime object to the user's timezone.
    
    Args:
        dt: The datetime object to convert
        user_timezone: The target timezone (e.g., "America/New_York")
        
    Returns:
        A datetime object in the user's timezone
    """
    try:
        user_tz = zoneinfo.ZoneInfo(user_timezone)
        if dt.tzinfo is None:
            # Assume UTC if no timezone info
            utc_tz = zoneinfo.ZoneInfo("UTC")
            dt = dt.replace(tzinfo=utc_tz)
        return dt.astimezone(user_tz)
    except Exception:
        # Fallback to UTC if timezone is invalid
        utc_tz = zoneinfo.ZoneInfo("UTC")
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=utc_tz)
        return dt.astimezone(utc_tz)

def convert_to_utc(dt: datetime, user_timezone: str = "UTC") -> datetime:
    """
    Convert a datetime object from the user's timezone to UTC.
    
    Args:
        dt: The datetime object to convert
        user_timezone: The source timezone (e.g., "America/New_York")
        
    Returns:
        A datetime object in UTC
    """
    try:
        user_tz = zoneinfo.ZoneInfo(user_timezone)
        if dt.tzinfo is None:
            # Assume user timezone if no timezone info
            dt = user_tz.localize(dt)
        return dt.astimezone(zoneinfo.ZoneInfo("UTC"))
    except Exception:
        # Fallback: if timezone is invalid, assume it's already in UTC
        if dt.tzinfo is None:
            return dt.replace(tzinfo=zoneinfo.ZoneInfo("UTC"))
        return dt.astimezone(zoneinfo.ZoneInfo("UTC"))

def get_current_time_in_timezone(user_timezone: str = "UTC") -> datetime:
    """
    Get the current time in the user's timezone.
    
    Args:
        user_timezone: The target timezone (e.g., "America/New_York")
        
    Returns:
        Current datetime in the user's timezone
    """
    utc_now = datetime.now(zoneinfo.ZoneInfo("UTC"))
    return convert_to_user_timezone(utc_now, user_timezone)

def validate_timezone(timezone_str: str) -> bool:
    """
    Validate if a timezone string is valid.
    
    Args:
        timezone_str: The timezone string to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        zoneinfo.ZoneInfo(timezone_str)
        return True
    except Exception:
        return False