from datetime import date, timedelta, datetime
from typing import List, Optional
import calendar

def calculate_next_due_date(
    current_due_date: date,
    recurrence_type: str,
    recurrence_days: Optional[List[str]] = None,
    end_date: Optional[date] = None
) -> Optional[date]:
    """
    Calculate the next due date based on the recurrence pattern.
    
    Args:
        current_due_date: The current due date
        recurrence_type: Type of recurrence ('daily', 'weekly', 'monthly')
        recurrence_days: Days of the week for weekly recurrence (e.g., ['monday', 'wednesday'])
        end_date: Optional end date for the recurrence
        
    Returns:
        The next due date, or None if end_date is reached
    """
    next_date = None
    
    if recurrence_type == "daily":
        next_date = current_due_date + timedelta(days=1)
    
    elif recurrence_type == "weekly":
        if recurrence_days:
            # Find the next occurrence of any of the specified days
            next_date = _find_next_weekday(current_due_date, recurrence_days)
        else:
            # Default to same day of week if no specific days specified
            next_date = current_due_date + timedelta(weeks=1)
    
    elif recurrence_type == "monthly":
        # Calculate next month, handling month-end edge cases
        next_date = _add_months(current_due_date, 1)
    
    # Check if the next date exceeds the end date
    if end_date and next_date and next_date > end_date:
        return None
    
    return next_date

def _find_next_weekday(current_date: date, target_days: List[str]) -> date:
    """
    Find the next occurrence of any of the specified weekdays.
    
    Args:
        current_date: The starting date
        target_days: List of target weekdays (e.g., ['monday', 'wednesday'])
        
    Returns:
        The next date matching one of the target days
    """
    # Map day names to numbers (Monday=0, Sunday=6)
    day_map = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
        'friday': 4, 'saturday': 5, 'sunday': 6
    }
    
    # Convert target days to numbers
    target_day_numbers = [day_map[day.lower()] for day in target_days if day.lower() in day_map]
    
    # Start from the next day
    check_date = current_date + timedelta(days=1)
    
    # Look ahead for up to 7 days to find the next occurrence
    for i in range(7):
        if check_date.weekday() in target_day_numbers:
            return check_date
        check_date += timedelta(days=1)
    
    # This shouldn't happen if target_day_numbers is valid, but just in case
    return current_date + timedelta(days=7)

def _add_months(source_date: date, months: int) -> date:
    """
    Add months to a date, handling month-end edge cases.
    
    Args:
        source_date: The starting date
        months: Number of months to add
        
    Returns:
        The resulting date after adding months
    """
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    
    # Handle month-end edge cases (e.g., Jan 31 + 1 month should be Feb 28/29, not Mar)
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    
    return date(year, month, day)

def is_leap_year(year: int) -> bool:
    """
    Check if a year is a leap year.
    
    Args:
        year: The year to check
        
    Returns:
        True if leap year, False otherwise
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def handle_february_29th(current_date: date) -> date:
    """
    Handle the special case of recurring tasks set for February 29th in non-leap years.
    
    Args:
        current_date: The current date (February 29th in a leap year)
        
    Returns:
        The appropriate date in the next year (February 28th if not a leap year)
    """
    next_year = current_date.year + 1
    if is_leap_year(next_year):
        # Next year is a leap year, so February 29th exists
        try:
            return date(next_year, 2, 29)
        except ValueError:
            # Fallback in case of error
            return date(next_year, 2, 28)
    else:
        # Next year is not a leap year, so use February 28th
        return date(next_year, 2, 28)

def calculate_recurring_instances(
    start_date: date,
    recurrence_type: str,
    recurrence_days: Optional[List[str]] = None,
    max_occurrences: Optional[int] = None,
    end_date: Optional[date] = None
) -> List[date]:
    """
    Calculate multiple recurring instances based on the recurrence pattern.
    
    Args:
        start_date: The initial date
        recurrence_type: Type of recurrence ('daily', 'weekly', 'monthly')
        recurrence_days: Days of the week for weekly recurrence
        max_occurrences: Maximum number of occurrences to generate
        end_date: Optional end date for the recurrence
        
    Returns:
        A list of dates representing the recurring instances
    """
    instances = []
    current_date = start_date
    
    occurrence_count = 0
    while True:
        # Check if we've reached the maximum occurrences
        if max_occurrences and occurrence_count >= max_occurrences:
            break
            
        # Check if we've passed the end date
        if end_date and current_date > end_date:
            break
            
        # Add the current date to the list
        instances.append(current_date)
        occurrence_count += 1
        
        # Calculate the next date
        next_date = calculate_next_due_date(
            current_date, 
            recurrence_type, 
            recurrence_days, 
            end_date
        )
        
        # If no next date (e.g., end date reached), break
        if next_date is None:
            break
            
        current_date = next_date
        
    return instances