import { Task } from '@/shared/types/types';
import { apiClient } from '@/shared/api/api';

interface ApiResponse<T> {
  data?: T;
  error?: string;
  success: boolean;
}

// Fetch all tasks for the current user
export const fetchTasks = async (): Promise<ApiResponse<Task[]>> => {
  try {
    // Using the apiClient which handles JWT tokens automatically
    const tasksResponse = await apiClient.request<{ data: Task[] }>('/api/v1/');
    return { data: tasksResponse.data, success: true };
  } catch (error) {
    console.error('Error fetching tasks:', error);
    return { error: error instanceof Error ? error.message : 'Failed to fetch tasks', success: false };
  }
};

// Create a new task
export const createTask = async (taskData: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>): Promise<ApiResponse<Task>> => {
  try {
    // Using the apiClient which handles JWT tokens automatically
    const newTask = await apiClient.request<Task>('/api/v1/', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
    return { data: newTask, success: true };
  } catch (error) {
    console.error('Error creating task:', error);
    return { error: error instanceof Error ? error.message : 'Failed to create task', success: false };
  }
};

// Update an existing task
export const updateTask = async (id: string, updates: Partial<Task>): Promise<ApiResponse<Task>> => {
  try {
    // Using the apiClient which handles JWT tokens automatically
    const updatedTask = await apiClient.request<Task>(`/api/v1/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
    return { data: updatedTask, success: true };
  } catch (error) {
    console.error('Error updating task:', error);
    return { error: error instanceof Error ? error.message : 'Failed to update task', success: false };
  }
};

// Delete a task
export const deleteTask = async (id: string): Promise<ApiResponse<null>> => {
  try {
    // Using the apiClient which handles JWT tokens automatically
    await apiClient.request<null>(`/api/v1/${id}`, {
      method: 'DELETE',
    });
    return { success: true };
  } catch (error) {
    console.error('Error deleting task:', error);
    return { error: error instanceof Error ? error.message : 'Failed to delete task', success: false };
  }
};

// Toggle task completion
export const toggleTaskCompletion = async (id: string, completed: boolean): Promise<ApiResponse<Task>> => {
  try {
    // Using the apiClient which handles JWT tokens automatically
    const updatedTask = await apiClient.request<Task>(`/api/v1/${id}/complete`, {
      method: 'PATCH',
      body: JSON.stringify({ completed }),
    });
    return { data: updatedTask, success: true };
  } catch (error) {
    console.error('Error toggling task completion:', error);
    return { error: error instanceof Error ? error.message : 'Failed to toggle task completion', success: false };
  }
};