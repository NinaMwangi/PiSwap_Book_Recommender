// src/services/api.js
import axios from 'axios';
import { EventEmitter } from 'events';

// Create event emitter for global error handling
export const apiEvents = new EventEmitter();

const MAX_RETRIES = 3;
const BASE_TIMEOUT = 10000;
const RETRY_DELAY = 1000;

const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: BASE_TIMEOUT,
});

// Track active requests for cancellation
const activeRequests = new Set();

// Add request to tracker
const addRequest = (config) => {
  const requestId = `${config.method}-${config.url}`;
  activeRequests.add(requestId);
  config.requestId = requestId;
  return config;
};

// Remove request from tracker
const removeRequest = (config) => {
  if (config?.requestId) {
    activeRequests.delete(config.requestId);
  }
};

// Cancel all active requests
export const cancelAllRequests = () => {
  activeRequests.forEach(id => {
    apiEvents.emit('requestCancelled', id);
  });
  activeRequests.clear();
};

// Unified response handler
const handleResponse = (response) => {
  removeRequest(response.config);
  
  // Handle empty responses
  if (!response.data) {
    throw new Error('Empty response from server');
  }

  // Handle string responses
  if (typeof response.data === 'string') {
    try {
      response.data = response.data ? JSON.parse(response.data) : {};
    } catch (e) {
      throw new Error(`Invalid JSON response: ${response.data}`);
    }
  }

  // Validate response structure
  if (typeof response.data !== 'object') {
    throw new Error('Invalid API response format');
  }

  // Handle API-specific error formats
  if (response.data.error) {
    throw new Error(response.data.error);
  }

  return response.data;
};

// Enhanced error handler with retry logic
const handleError = async (error) => {
  const config = error.config || {};
  removeRequest(config);

  let message = 'Request failed';
  let status = null;
  let shouldRetry = false;
  let details = null;

  if (error.response) {
    // Server responded with error status
    status = error.response.status;
    details = error.response.data?.detail || error.response.data;
    message = `API Error: ${status} - ${details?.message || error.response.statusText}`;
    
    // Retry only on these status codes
    shouldRetry = [502, 503, 504].includes(status) && 
      (config.retryCount || 0) < MAX_RETRIES;
  } 
  else if (error.code === 'ECONNABORTED') {
    message = 'Request timed out';
    shouldRetry = (config.retryCount || 0) < MAX_RETRIES;
  } 
  else if (error.message === 'Network Error') {
    message = 'Network error - No response received';
    shouldRetry = (config.retryCount || 0) < MAX_RETRIES;
  } 
  else {
    message = error.message || 'Unknown API error';
  }

  // Emit global error event
  apiEvents.emit('apiError', { 
    message, 
    status, 
    details, 
    url: config.url,
    method: config.method
  });

  // Retry logic
  if (shouldRetry) {
    const retryCount = (config.retryCount || 0) + 1;
    const delay = RETRY_DELAY * retryCount;
    
    await new Promise(resolve => setTimeout(resolve, delay));
    
    return API({
      ...config,
      retryCount,
      timeout: BASE_TIMEOUT * (retryCount + 1)
    });
  }

  throw new Error(message);
};

// Request interceptor
API.interceptors.request.use(config => {
  return addRequest(config);
}, error => {
  return Promise.reject(error);
});

// Response interceptor
API.interceptors.response.use(
  response => handleResponse(response),
  error => handleError(error)
);

const apiService = {
  /**
   * Upload CSV file with progress tracking
   */
  async uploadCSV(file, onProgress) {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const response = await API.post('/api/upload', formData, {
        onUploadProgress: (progressEvent) => {
          if (onProgress && progressEvent.total) {
            const percent = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            onProgress(percent);
          }
        },
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 30000 // Longer timeout for file uploads
      });

      return {
        status: 'success',
        data: response.data,
        bookCount: response.data?.book_count || 0
      };
    } catch (error) {
      return {
        status: 'error',
        error: error.message,
        details: error.details
      };
    }
  },

  /**
   * Get book recommendations with retries
   */
  async getRecommendations(title) {
    
    try {
      const response = await API.get(
        `/api/recommend/${encodeURIComponent(title)}`,
        { timeout: 15000 }
      );
      

      return {
        status: 'success',
        books:response.recommendations,
        metadata: response.recommendations?.debug_info || {}
      };
    } catch (error) {
      return {
        status: 'error',
        error: error.message,
        books: [],
        fallback: true // Flag for UI to show cached data
      };
    }
  },

  /**
   * Get training status with heartbeat check
   */
  async getTrainingStatus() {
    try {
      const response = await API.get('/api/training-status', {
        timeout: 8000,
        headers: {
          'Cache-Control': 'no-cache'
        }
      });

      return {
        status: 'success',
        exists: Boolean(response.data?.model_exists),
        lastTrained: response.data?.last_trained || null,
        bookCount: response.data?.book_count || 0,
        isTraining: response.data?.is_training || false
      };
    } catch (error) {
      return {
        status: 'error',
        error: error.message,
        exists: false,
        lastTrained: null,
        bookCount: 0
      };
    }
  },

  /**
   * Health check endpoint
   */
  async checkHealth() {
    try {
      const response = await API.get('/api/health', { timeout: 3000 });
      return {
        online: true,
        database: response.data?.database === 'connected',
        timestamp: response.data?.timestamp
      };
    } catch (error) {
      return {
        online: false,
        error: error.message
      };
    }
  },

  /**
   * Cancel all pending requests
   */
  cancelAllRequests
};

export default apiService;