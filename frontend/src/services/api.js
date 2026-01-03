// API service for backend communication
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Generic request method
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Task-related methods
  async getTasks() {
    return this.request('/tasks');
  }

  async createTask(taskData) {
    return this.request('/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async updateTask(taskId, taskData) {
    return this.request(`/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(taskId) {
    return this.request(`/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  async completeTask(taskId, completed = true) {
    return this.request(`/tasks/${taskId}/complete`, {
      method: 'POST',
      body: JSON.stringify({ completed }),
    });
  }

  // Recurring task methods
  async createRecurringTask(taskId, recurrenceData) {
    return this.request('/recurring-tasks', {
      method: 'POST',
      body: JSON.stringify({
        task_id: taskId,
        ...recurrenceData
      }),
    });
  }

  async getRecurringTask(recurringTaskId) {
    return this.request(`/recurring-tasks/${recurringTaskId}`);
  }

  async updateRecurringTask(recurringTaskId, recurrenceData) {
    return this.request(`/recurring-tasks/${recurringTaskId}`, {
      method: 'PUT',
      body: JSON.stringify(recurrenceData),
    });
  }

  async deleteRecurringTask(recurringTaskId) {
    return this.request(`/recurring-tasks/${recurringTaskId}`, {
      method: 'DELETE',
    });
  }

  // Reminder methods
  async scheduleReminder(reminderData) {
    return this.request('/reminders', {
      method: 'POST',
      body: JSON.stringify(reminderData),
    });
  }

  async getReminder(reminderId) {
    return this.request(`/reminders/${reminderId}`);
  }

  async getRemindersForTask(taskId) {
    return this.request(`/reminders?task_id=${taskId}`);
  }

  async getUpcomingReminders(limit = 10) {
    return this.request(`/reminders/upcoming?limit=${limit}`);
  }

  async markReminderAsSent(reminderId) {
    return this.request(`/reminders/${reminderId}/sent`, {
      method: 'PUT',
    });
  }

  async cancelReminder(reminderId) {
    return this.request(`/reminders/${reminderId}`, {
      method: 'DELETE',
    });
  }
}

export default new ApiService();