import React, { useState } from 'react';

const RecurrencePicker = ({ recurrence, onChange }) => {
  const [recurrenceType, setRecurrenceType] = useState(recurrence?.type || 'daily');
  const [recurrenceDays, setRecurrenceDays] = useState(recurrence?.days || []);
  const [endDate, setEndDate] = useState(recurrence?.endDate || '');

  const handleDayToggle = (day) => {
    let updatedDays;
    if (recurrenceDays.includes(day)) {
      updatedDays = recurrenceDays.filter(d => d !== day);
    } else {
      updatedDays = [...recurrenceDays, day];
    }
    setRecurrenceDays(updatedDays);
    onChange({ type: recurrenceType, days: updatedDays, endDate });
  };

  const handleTypeChange = (type) => {
    setRecurrenceType(type);
    // Reset days when changing to daily or monthly
    if (type !== 'weekly') {
      setRecurrenceDays([]);
      onChange({ type, days: [], endDate });
    } else {
      onChange({ type, days: recurrenceDays, endDate });
    }
  };

  const handleEndDateChange = (date) => {
    setEndDate(date);
    onChange({ type: recurrenceType, days: recurrenceDays, endDate: date });
  };

  return (
    <div className="recurrence-picker">
      <h3>Recurrence Settings</h3>
      
      <div className="form-group">
        <label>Recurrence Pattern</label>
        <div className="recurrence-options">
          <label>
            <input
              type="radio"
              value="daily"
              checked={recurrenceType === 'daily'}
              onChange={() => handleTypeChange('daily')}
            />
            Daily
          </label>
          <label>
            <input
              type="radio"
              value="weekly"
              checked={recurrenceType === 'weekly'}
              onChange={() => handleTypeChange('weekly')}
            />
            Weekly
          </label>
          <label>
            <input
              type="radio"
              value="monthly"
              checked={recurrenceType === 'monthly'}
              onChange={() => handleTypeChange('monthly')}
            />
            Monthly
          </label>
        </div>
      </div>

      {recurrenceType === 'weekly' && (
        <div className="form-group">
          <label>Days of the Week</label>
          <div className="weekdays">
            {['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'].map(day => (
              <label key={day} className="weekday-option">
                <input
                  type="checkbox"
                  checked={recurrenceDays.includes(day)}
                  onChange={() => handleDayToggle(day)}
                />
                {day.charAt(0).toUpperCase() + day.slice(1)}
              </label>
            ))}
          </div>
        </div>
      )}

      <div className="form-group">
        <label htmlFor="endDate">End Date (optional)</label>
        <input
          type="date"
          id="endDate"
          value={endDate}
          onChange={(e) => handleEndDateChange(e.target.value)}
        />
      </div>

      <div className="recurrence-summary">
        <p>
          Recurring: <strong>{recurrenceType}</strong>
          {recurrenceType === 'weekly' && recurrenceDays.length > 0 && (
            <span> on {recurrenceDays.join(', ')}</span>
          )}
          {endDate && <span>, ending on {new Date(endDate).toLocaleDateString()}</span>}
        </p>
      </div>
    </div>
  );
};

export default RecurrencePicker;