import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { userAPI } from '../services/api';

export default function AccountPage() {
  const { t, i18n } = useTranslation();
  const [profile, setProfile] = useState(null);
  const [openAIConfig, setOpenAIConfig] = useState({
    api_key: '',
    api_url: 'https://api.openai.com/v1',
    model: 'gpt-3.5-turbo',
  });
  const [settings, setSettings] = useState({
    language: i18n.language,
    dark_mode: localStorage.getItem('darkMode') === 'true',
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    loadProfile();
    loadOpenAIConfig();
  }, []);

  const loadProfile = async () => {
    try {
      const response = await userAPI.getProfile();
      setProfile(response.data);
    } catch (error) {
      console.error('Failed to load profile:', error);
    }
  };

  const loadOpenAIConfig = async () => {
    try {
      const response = await userAPI.getOpenAIConfig();
      setOpenAIConfig(response.data);
    } catch (error) {
      console.error('Failed to load OpenAI config:', error);
    }
  };

  const handleOpenAIChange = (e) => {
    const { name, value } = e.target;
    setOpenAIConfig(prev => ({ ...prev, [name]: value }));
  };

  const handleSettingsChange = (e) => {
    const { name, type, checked, value } = e.target;
    setSettings(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSaveOpenAI = async () => {
    setLoading(true);
    try {
      await userAPI.setOpenAIConfig({
        api_key: openAIConfig.api_key,
        api_url: openAIConfig.api_url,
        model: openAIConfig.model,
      });
      setMessage('OpenAI settings saved!');
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage('Failed to save settings: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleSaveSettings = async () => {
    setLoading(true);
    try {
      // Change language
      if (settings.language !== i18n.language) {
        i18n.changeLanguage(settings.language);
        localStorage.setItem('language', settings.language);
      }

      // Save to backend
      await userAPI.updateSettings({
        language: settings.language,
        dark_mode: settings.dark_mode,
      });

      // Update dark mode
      if (settings.dark_mode) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
      localStorage.setItem('darkMode', settings.dark_mode);

      setMessage('Settings saved!');
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage('Failed to save settings: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  if (!profile) {
    return (
      <div className="flex-1 p-6 flex items-center justify-center">
        <p>{t('common.loading')}</p>
      </div>
    );
  }

  return (
    <div className="flex-1 p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
          {t('nav.account')}
        </h1>

        {message && (
          <div className="mb-6 p-4 bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-100 rounded-lg">
            {message}
          </div>
        )}

        {/* Profile Info */}
        <div className="bg-white dark:bg-slate-800 rounded-lg shadow p-6 mb-6 border border-gray-200 dark:border-slate-700">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Profile</h2>
          <div className="space-y-3">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Username</p>
              <p className="text-lg font-semibold text-gray-900 dark:text-white">
                {profile.username}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Email</p>
              <p className="text-lg font-semibold text-gray-900 dark:text-white">
                {profile.email}
              </p>
            </div>
          </div>
        </div>

        {/* OpenAI Configuration */}
        <div className="bg-white dark:bg-slate-800 rounded-lg shadow p-6 mb-6 border border-gray-200 dark:border-slate-700">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">OpenAI API Configuration</h2>
          
          <div className="mb-4">
            <label className="block text-gray-700 dark:text-gray-300 text-sm font-bold mb-2">
              {t('account.apiKey')}
            </label>
            <input
              type="password"
              name="api_key"
              value={openAIConfig.api_key}
              onChange={handleOpenAIChange}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="sk-..."
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-700 dark:text-gray-300 text-sm font-bold mb-2">
              {t('account.apiUrl')}
            </label>
            <input
              type="text"
              name="api_url"
              value={openAIConfig.api_url}
              onChange={handleOpenAIChange}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="https://api.openai.com/v1"
            />
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 dark:text-gray-300 text-sm font-bold mb-2">
              {t('account.model')}
            </label>
            <select
              name="model"
              value={openAIConfig.model}
              onChange={handleOpenAIChange}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
              <option value="gpt-4">GPT-4</option>
              <option value="gpt-4-turbo">GPT-4 Turbo</option>
            </select>
          </div>

          <button
            onClick={handleSaveOpenAI}
            disabled={loading}
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-6 rounded-lg transition disabled:opacity-50"
          >
            {loading ? t('common.loading') : t('account.save')}
          </button>
        </div>

        {/* Settings */}
        <div className="bg-white dark:bg-slate-800 rounded-lg shadow p-6 border border-gray-200 dark:border-slate-700">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
            {t('nav.settings')}
          </h2>

          <div className="mb-6">
            <label className="block text-gray-700 dark:text-gray-300 text-sm font-bold mb-2">
              {t('account.language')}
            </label>
            <select
              name="language"
              value={settings.language}
              onChange={handleSettingsChange}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="en">English</option>
              <option value="zh">中文</option>
            </select>
          </div>

          <div className="mb-6 flex items-center">
            <input
              type="checkbox"
              id="dark_mode"
              name="dark_mode"
              checked={settings.dark_mode}
              onChange={handleSettingsChange}
              className="w-4 h-4 text-indigo-600 rounded focus:ring-indigo-500 cursor-pointer"
            />
            <label htmlFor="dark_mode" className="ml-3 text-gray-700 dark:text-gray-300 cursor-pointer">
              {t('account.darkMode')}
            </label>
          </div>

          <button
            onClick={handleSaveSettings}
            disabled={loading}
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-6 rounded-lg transition disabled:opacity-50"
          >
            {loading ? t('common.loading') : t('account.save')}
          </button>
        </div>
      </div>
    </div>
  );
}
