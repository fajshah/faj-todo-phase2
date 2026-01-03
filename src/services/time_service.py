from datetime import datetime, date, time, timedelta
from typing import Optional
import zoneinfo
from src.utils.timezone_utils import convert_to_user_timezone, convert_to_utc, validate_timezone

class TimeService:
    """
    Service class to handle time zone and date/time operations.
    """
    
    def __init__(self):
        pass
    
    def get_current_time_in_user_timezone(self, user_timezone: str = "UTC") -> datetime:
        """
        Get the current time in the user's timezone.
        
        Args:
            user_timezone: The user's timezone (e.g., "America/New_York")
            
        Returns:
            Current datetime in the user's timezone
        """
        if not validate_timezone(user_timezone):
            user_timezone = "UTC"  # Fallback to UTC if invalid timezone
            
        utc_now = datetime.now(zoneinfo.ZoneInfo("UTC"))
        return convert_to_user_timezone(utc_now, user_timezone)
    
    def convert_datetime_to_user_timezone(
        self, 
        dt: datetime, 
        user_timezone: str = "UTC"
    ) -> datetime:
        """
        Convert a datetime object to the user's timezone.
        
        Args:
            dt: The datetime to convert
            user_timezone: The user's timezone
            
        Returns:
            The datetime in the user's timezone
        """
        if not validate_timezone(user_timezone):
            user_timezone = "UTC"  # Fallback to UTC if invalid timezone
            
        return convert_to_user_timezone(dt, user_timezone)
    
    def convert_datetime_to_utc(
        self, 
        dt: datetime, 
        user_timezone: str = "UTC"
    ) -> datetime:
        """
        Convert a datetime object from the user's timezone to UTC.
        
        Args:
            dt: The datetime to convert
            user_timezone: The user's timezone
            
        Returns:
            The datetime in UTC
        """
        if not validate_timezone(user_timezone):
            user_timezone = "UTC"  # Fallback to UTC if invalid timezone
            
        return convert_to_utc(dt, user_timezone)
    
    def handle_dst_transitions(
        self, 
        dt: datetime, 
        user_timezone: str
    ) -> datetime:
        """
        Handle daylight saving time transitions for a datetime in a specific timezone.
        
        Args:
            dt: The datetime to handle DST for
            user_timezone: The user's timezone
            
        Returns:
            The datetime adjusted for DST if necessary
        """
        if not validate_timezone(user_timezone):
            return dt  # Return as is if timezone is invalid
            
        try:
            user_tz = zoneinfo.ZoneInfo(user_timezone)
            
            # Localize the datetime to the user's timezone
            if dt.tzinfo is None:
                localized_dt = user_tz.localize(dt)
            else:
                localized_dt = dt.astimezone(user_tz)
                
            return localized_dt
        except Exception:
            # If there's an error, return the original datetime
            return dt
    
    def adjust_for_timezone_change(
        self,
        original_datetime: datetime,
        original_timezone: str,
        new_timezone: str
    ) -> datetime:
        """
        Adjust a datetime when the user changes timezones.
        
        Args:
            original_datetime: The original datetime in the original timezone
            original_timezone: The original timezone
            new_timezone: The new timezone
            
        Returns:
            The datetime adjusted for the new timezone
        """
        # First, convert the original datetime to UTC
        utc_datetime = self.convert_datetime_to_utc(original_datetime, original_timezone)
        
        # Then, convert from UTC to the new timezone
        new_datetime = self.convert_datetime_to_user_timezone(utc_datetime, new_timezone)
        
        return new_datetime