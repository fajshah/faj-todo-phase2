import React, { useState } from 'react';

const ReminderPicker = ({ reminder, onChange }) => {
  const [reminderTime, setReminderTime] = useState(reminder?.time || '');
  const [reminderOption, setReminderOption] = useState(reminder?.option || 'none');

  const reminderOptions = [
    { value: 'none', label: 'No reminder' },
    { value: '10min', label: '10 minutes before' },
    { value: '30min', label: '30 minutes before' },
    { value: '1hour', label: '1 hour before' },
    { value: '1day', label: '1 day before' },
    { value: 'custom', label: 'Custom time' },
  ];

  const calculateCustomTime = () => {
    if (!reminderTime) return null;
    
    const taskDueDateTime = new Date(reminderTime);
    return taskDueDateTime.toISOString();
  };

  const handleOptionChange = (option) => {
    setReminderOption(option);
    
    if (option === 'custom') {
      onChange({ option, time: reminderTime });
    } else if (option !== 'none') {
      // Calculate the appropriate reminder time based on the option
      // This would be implemented based on the task's due date/time
      onChange({ option, time: calculateCustomTime() });
    } else {
      onChange({ option: 'none', time: null });
    }
  };

  const handleCustomTimeChange = (time) => {
    setReminderTime(time);
    
    if (reminderOption === 'custom') {
      onChange({ option: 'custom', time });
    }
  };

  return (
    <div className="reminder-picker">
      <h3>Reminder Settings</h3>
      
      <div className="form-group">
        <label htmlFor="reminderOption">Reminder</label>
        <select
          id="reminderOption"
          value={reminderOption}
          onChange={(e) => handleOptionChange(e.target.value)}
        >
          {reminderOptions.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>

      {reminderOption === 'custom' && (
        <div className="form-group">
          <label htmlFor="customReminderTime">Custom Reminder Time</label>
          <input
            type="datetime-local"
            id="customReminderTime"
            value={reminderTime}
            onChange={(e) => handleCustomTimeChange(e.target.value)}
          />
        </div>
      )}

      <div className="reminder-summary">
        {reminderOption !== 'none' ? (
          <p>
            Reminder set for: <strong>
              {reminderOption === 'custom' 
                ? new Date(reminderTime).toLocaleString() 
                : reminderOption}
            </strong>
          </p>
        ) : (
          <p>No reminder set</p>
        )}
      </div>
    </div>
  );
};

export default ReminderPicker;