"""Frontend configuration"""
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export const LANGUAGES = {
  EN: 'en',
  ZH: 'zh'
};

export const THEMES = {
  LIGHT: 'light',
  DARK: 'dark'
};

export const DEFAULT_CONFIG = {
  language: 'en',
  theme: 'light',
  itemsPerPage: 20
};
