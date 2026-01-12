// API service for handling all backend requests

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:5000/api';

// Helper function to get auth token
const getAuthToken = () => {
  return localStorage.getItem('token');
};

// Generic request function
const request = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  const token = getAuthToken();
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const config = {
    headers,
    ...options,
  };

  const response = await fetch(url, config);

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
  }

  return response.json();
};

// Authentication API functions
export const authAPI = {
  register: (userData) => request('/auth/register', {
    method: 'POST',
    body: JSON.stringify(userData),
  }),

  login: (credentials) => request('/auth/login', {
    method: 'POST',
    body: JSON.stringify(credentials),
  }),
};

// Todo API functions
export const todoAPI = {
  getAll: (params = {}) => {
    const queryParams = new URLSearchParams(params);
    return request(`/todos?${queryParams.toString()}`);
  },

  getById: (id) => request(`/todos/${id}`),

  create: (todoData) => request('/todos', {
    method: 'POST',
    body: JSON.stringify(todoData),
  }),

  update: (id, todoData) => request(`/todos/${id}`, {
    method: 'PUT',
    body: JSON.stringify(todoData),
  }),

  delete: (id) => request(`/todos/${id}`, {
    method: 'DELETE',
  }),
};

export default {
  authAPI,
  todoAPI,
};