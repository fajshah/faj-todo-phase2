import React, { useState } from 'react';

const TaskForm = ({ onSubmit }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [dueTime, setDueTime] = useState('');
  const [priority, setPriority] = useState('medium');
  const [isRecurring, setIsRecurring] = useState(false);
  const [recurrenceType, setRecurrenceType] = useState('daily');
  const [recurrenceDays, setRecurrenceDays] = useState([]);
  const [reminderTime, setReminderTime] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const taskData = {
      title,
      description,
      dueDate: dueDate || null,
      dueTime: dueTime || null,
      priority,
      isRecurring,
    };
    
    // Add recurrence data if task is recurring
    if (isRecurring) {
      taskData.recurrence = {
        type: recurrenceType,
        days: recurrenceType === 'weekly' ? recurrenceDays : null,
      };
    }
    
    // Add reminder data if specified
    if (reminderTime) {
      taskData.reminder = {
        time: reminderTime,
        type: 'browser',
      };
    }
    
    onSubmit(taskData);
    
    // Reset form
    setTitle('');
    setDescription('');
    setDueDate('');
    setDueTime('');
    setPriority('medium');
    setIsRecurring(false);
    setRecurrenceType('daily');
    setRecurrenceDays([]);
    setReminderTime('');
  };

  const handleDayToggle = (day) => {
    if (recurrenceDays.includes(day)) {
      setRecurrenceDays(recurrenceDays.filter(d => d !== day));
    } else {
      setRecurrenceDays([...recurrenceDays, day]);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="task-form">
      <div className="form-group">
        <label htmlFor="title">Title *</label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </div>

      <div className="form-group">
        <label htmlFor="dueDate">Due Date</label>
        <input
          type="date"
          id="dueDate"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
        />
      </div>

      <div className="form-group">
        <label htmlFor="dueTime">Due Time</label>
        <input
          type="time"
          id="dueTime"
          value={dueTime}
          onChange={(e) => setDueTime(e.target.value)}
        />
      </div>

      <div className="form-group">
        <label htmlFor="priority">Priority</label>
        <select
          id="priority"
          value={priority}
          onChange={(e) => setPriority(e.target.value)}
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>

      <div className="form-group">
        <label>
          <input
            type="checkbox"
            checked={isRecurring}
            onChange={(e) => setIsRecurring(e.target.checked)}
          />
          Make this task recurring
        </label>
      </div>

      {isRecurring && (
        <div className="recurring-options">
          <div className="form-group">
            <label>Recurrence Type</label>
            <div>
              <label>
                <input
                  type="radio"
                  value="daily"
                  checked={recurrenceType === 'daily'}
                  onChange={(e) => setRecurrenceType(e.target.value)}
                />
                Daily
              </label>
              <label>
                <input
                  type="radio"
                  value="weekly"
                  checked={recurrenceType === 'weekly'}
                  onChange={(e) => setRecurrenceType(e.target.value)}
                />
                Weekly
              </label>
              <label>
                <input
                  type="radio"
                  value="monthly"
                  checked={recurrenceType === 'monthly'}
                  onChange={(e) => setRecurrenceType(e.target.value)}
                />
                Monthly
              </label>
            </div>
          </div>

          {recurrenceType === 'weekly' && (
            <div className="form-group">
              <label>Days of the week</label>
              {['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'].map(day => (
                <label key={day}>
                  <input
                    type="checkbox"
                    checked={recurrenceDays.includes(day)}
                    onChange={() => handleDayToggle(day)}
                  />
                  {day.charAt(0).toUpperCase() + day.slice(1)}
                </label>
              ))}
            </div>
          )}
        </div>
      )}

      <div className="form-group">
        <label htmlFor="reminderTime">Reminder Time</label>
        <input
          type="datetime-local"
          id="reminderTime"
          value={reminderTime}
          onChange={(e) => setReminderTime(e.target.value)}
        />
      </div>

      <button type="submit">Create Task</button>
    </form>
  );
};

export default TaskForm;