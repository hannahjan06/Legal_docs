// Mock authentication system using localStorage
export interface User {
  email: string;
  name: string;
}

export const mockAuth = {
  // Mock login - just validates email format and any password
  login: async (email: string, password: string): Promise<User> => {
    // Simple email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      throw new Error('Invalid email format');
    }
    
    if (!password || password.length < 1) {
      throw new Error('Password is required');
    }

    // Create mock user
    const user: User = {
      email,
      name: email.split('@')[0], // Use email prefix as name
    };

    // Store in localStorage
    localStorage.setItem('auth_user', JSON.stringify(user));
    return user;
  },

  // Mock signup - similar to login but validates password confirmation
  signup: async (email: string, password: string, confirmPassword: string): Promise<User> => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      throw new Error('Invalid email format');
    }
    
    if (!password || password.length < 6) {
      throw new Error('Password must be at least 6 characters');
    }

    if (password !== confirmPassword) {
      throw new Error('Passwords do not match');
    }

    // Create mock user
    const user: User = {
      email,
      name: email.split('@')[0],
    };

    // Store in localStorage
    localStorage.setItem('auth_user', JSON.stringify(user));
    return user;
  },

  // Get current user from localStorage
  getCurrentUser: (): User | null => {
    const userStr = localStorage.getItem('auth_user');
    return userStr ? JSON.parse(userStr) : null;
  },

  // Logout - remove from localStorage
  logout: (): void => {
    localStorage.removeItem('auth_user');
  },

  // Check if user is authenticated
  isAuthenticated: (): boolean => {
    return localStorage.getItem('auth_user') !== null;
  }
};