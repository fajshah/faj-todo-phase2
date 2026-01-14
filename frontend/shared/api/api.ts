// API client abstraction for JWT handling and API requests

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://fajji-backend-todo.hf.space/api';

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  // Helper method to get JWT token from storage
  // NOTE: In a Better Auth integration, this would get the token from Better Auth context
  private getToken(): string | null {
    if (typeof window !== 'undefined') {
      // In a real Better Auth integration, this would get the token from Better Auth
      // For now, keeping localStorage as a fallback
      return localStorage.getItem('jwt_token');
    }
    return null;
  }

  // Helper method to set JWT token in storage
  // NOTE: In a Better Auth integration, this would set the token in Better Auth context
  private setToken(token: string): void {
    if (typeof window !== 'undefined') {
      // In a real Better Auth integration, this would set the token in Better Auth
      // For now, keeping localStorage as a fallback
      localStorage.setItem('jwt_token', token);
    }
  }

  // Helper method to remove JWT token from storage
  // NOTE: In a Better Auth integration, this would clear the Better Auth session
  private removeToken(): void {
    if (typeof window !== 'undefined') {
      // In a real Better Auth integration, this would clear the Better Auth session
      // For now, keeping localStorage as a fallback
      localStorage.removeItem('jwt_token');
    }
  }

  // Generic request method with JWT handling
  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    // Add JWT token to headers if available
    const token = this.getToken();
    if (token) {
      (config.headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, config);

      // Handle token expiration (401 Unauthorized)
      if (response.status === 401) {
        this.removeToken();
        // Optionally redirect to login page or show session expired message
        throw new Error('Session expired. Please log in again.');
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Network error. Please check your connection.');
      }
      throw error;
    }
  }

  // Authentication methods - These should be handled by Better Auth separately
  // For integration with Better Auth, these methods would need to be updated
  // to use Better Auth's API instead of backend endpoints
  async login(credentials: { email: string; password: string }): Promise<{ token: string; user: any }> {
    // In a real integration, this would call Better Auth API directly
    // For now, we'll keep the existing implementation but note this needs to be updated
    const response = await this.request<{ token: string; user: any }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });

    if (response.token) {
      this.setToken(response.token);
    }

    return response;
  }

  async signup(userData: { email: string; password: string; name: string }): Promise<{ token: string; user: any }> {
    // In a real integration, this would call Better Auth API directly
    // For now, we'll keep the existing implementation but note this needs to be updated
    const response = await this.request<{ token: string; user: any }>('/auth/signup', {
      method: 'POST',
      body: JSON.stringify(userData),
    });

    if (response.token) {
      this.setToken(response.token);
    }

    return response;
  }

  async logout(): Promise<void> {
    this.removeToken();
  }

  // Task methods - Updated to use backend API endpoints
  async getTasks(): Promise<{ tasks: any[] }> {
    return this.request<{ tasks: any[] }>('/todos');
  }

  async createTask(taskData: Omit<any, 'id'>): Promise<any> {
    return this.request<any>('/todos', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async updateTask(id: string, taskData: Partial<any>): Promise<any> {
    return this.request<any>(`/todos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(id: string): Promise<void> {
    await this.request<void>(`/todos/${id}`, {
      method: 'DELETE',
    });
  }

  async forgotPassword(email: string): Promise<{ message: string }> {
    // In a real integration, this would call Better Auth API directly
    // For now, we'll keep the existing implementation but note this needs to be updated
    return this.request<{ message: string }>('/auth/forgot-password', {
      method: 'POST',
      body: JSON.stringify({ email }),
    });
  }
}

export const apiClient = new ApiClient();