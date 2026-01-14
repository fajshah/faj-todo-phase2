import React, { useState, useEffect } from 'react';

const TaskList = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch tasks from API
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      // In a real implementation, this would fetch from the backend API
      // const response = await fetch('/api/v1/tasks');
      // const data = await response.json();
      // setTasks(data);
      
      // For now, using mock data
      setTasks([
        {
          id: 1,
          title: "Weekly Team Meeting",
          description: "Team sync meeting every Monday",
          completed: false,
          dueDate: "2023-10-02",
          dueTime: "10:00",
          priority: "high",
          isRecurring: true,
          recurrence: {
            type: "weekly",
            days: ["monday"]
          }
        },
        {
          id: 2,
          title: "Submit monthly report",
          description: "Monthly status report for management",
          completed: false,
          dueDate: "2023-10-01",
          dueTime: "17:00",
          priority: "medium",
          isRecurring: true,
          recurrence: {
            type: "monthly"
          }
        },
        {
          id: 3,
          title: "Daily exercise",
          description: "30 minutes of cardio",
          completed: true,
          dueDate: "2023-09-30",
          priority: "low",
          isRecurring: true,
          recurrence: {
            type: "daily"
          }
        }
      ]);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleTaskCompletion = async (taskId) => {
    try {
      // In a real implementation, this would call the backend API
      // await fetch(`/api/v1/tasks/${taskId}/complete`, { method: 'POST' });
      
      // Update local state
      setTasks(tasks.map(task => 
        task.id === taskId ? { ...task, completed: !task.completed } : task
      ));
    } catch (error) {
      console.error('Error toggling task completion:', error);
    }
  };

  if (loading) {
    return <div>Loading tasks...</div>;
  }

  return (
    <div className="task-list">
      <h2>Tasks</h2>
      {tasks.length === 0 ? (
        <p>No tasks found.</p>
      ) : (
        <ul>
          {tasks.map(task => (
            <li key={task.id} className={`task-item ${task.completed ? 'completed' : ''}`}>
              <div className="task-header">
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => toggleTaskCompletion(task.id)}
                />
                <h3>{task.title}</h3>
                <span className={`priority priority-${task.priority}`}>{task.priority}</span>
                {task.isRecurring && (
                  <span className="recurring-badge">Recurring: {task.recurrence.type}</span>
                )}
              </div>
              <div className="task-details">
                <p>{task.description}</p>
                {task.dueDate && (
                  <div className="due-date">
                    Due: {new Date(task.dueDate).toLocaleDateString()} 
                    {task.dueTime && ` at ${task.dueTime}`}
                  </div>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TaskList;