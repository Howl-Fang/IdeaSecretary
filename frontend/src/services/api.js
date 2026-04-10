import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  register: (username, email, password) =>
    api.post('/auth/register', { username, email, password }),
  login: (username, password) =>
    api.post('/auth/login', { username, password }),
  verify: () => api.get('/auth/verify'),
};

export const userAPI = {
  getProfile: () => api.get('/user/profile'),
  updateSettings: (settings) =>
    api.put('/user/settings', settings),
  getOpenAIConfig: () => api.get('/user/openai-config'),
  setOpenAIConfig: (config) =>
    api.post('/user/openai-config', config),
  getStatistics: () => api.get('/user/statistics'),
};

export const ideasAPI = {
  getBases: () => api.get('/ideas/bases'),
  getTree: (baseId) => api.get(`/ideas/${baseId}`),
  getIdea: (ideaId) => api.get(`/ideas/${ideaId}`),
  createIdea: (baseId, data) =>
    api.post(`/ideas/${baseId}/create`, data),
  updateIdea: (ideaId, data) =>
    api.put(`/ideas/${ideaId}`, data),
  deleteIdea: (ideaId) =>
    api.delete(`/ideas/${ideaId}`),
};

export const mediaAPI = {
  upload: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/media/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  getMedia: (mediaId) => api.get(`/media/${mediaId}`),
  deleteMedia: (mediaId) => api.delete(`/media/${mediaId}`),
  getTrash: () => api.get('/media/trash'),
  cleanupTrash: () => api.post('/media/trash/cleanup'),
  getMediaList: () => api.get('/media/info'),
};

export const searchAPI = {
  search: (query, baseId, limit = 20) =>
    api.get('/search', { params: { q: query, base_id: baseId, limit } }),
};

export default api;
