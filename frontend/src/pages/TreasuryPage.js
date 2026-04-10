import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { ideasAPI, userAPI } from '../services/api';
import { FileText, Plus, Search } from 'lucide-react';

export default function TreasuryPage() {
  const { t } = useTranslation();
  const [content, setContent] = useState('');
  const [title, setTitle] = useState('');
  const [baseId, setBaseId] = useState(null);
  const [bases, setBases] = useState([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    loadBases();
    loadStats();
  }, []);

  const loadBases = async () => {
    try {
      const response = await ideasAPI.getBases();
      setBases(response.data.bases);
      if (response.data.bases.length > 0) {
        setBaseId(response.data.bases[0].id);
      }
    } catch (error) {
      console.error('Failed to load bases:', error);
    }
  };

  const loadStats = async () => {
    try {
      const response = await userAPI.getStatistics();
      setStats(response.data);
    } catch (error) {
      console.error('Failed to load stats:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim() || !content.trim() || !baseId) return;

    setLoading(true);
    try {
      await ideasAPI.createIdea(baseId, {
        title: title.trim(),
        content: content.trim(),
        tags: [],
      });
      setTitle('');
      setContent('');
      loadStats();
      // Show success message
      alert('Idea created successfully!');
    } catch (error) {
      alert('Failed to create idea: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
          {t('nav.treasury')}
        </h1>

        {/* Statistics */}
        {stats && (
          <div className="grid grid-cols-3 gap-4 mb-8">
            <div className="bg-white dark:bg-slate-800 rounded-lg p-4 border border-gray-200 dark:border-slate-700">
              <p className="text-gray-600 dark:text-gray-400 text-sm">{t('ideas.totalIdeas')}</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.total_ideas}</p>
            </div>
            <div className="bg-white dark:bg-slate-800 rounded-lg p-4 border border-gray-200 dark:border-slate-700">
              <p className="text-gray-600 dark:text-gray-400 text-sm">{t('ideas.totalWords')}</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.total_word_count}</p>
            </div>
            <div className="bg-white dark:bg-slate-800 rounded-lg p-4 border border-gray-200 dark:border-slate-700">
              <p className="text-gray-600 dark:text-gray-400 text-sm">{t('ideas.availableInspirations')}</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">—</p>
            </div>
          </div>
        )}

        {/* Idea Base Selector */}
        {bases.length > 0 && (
          <div className="mb-6">
            <label className="block text-gray-700 dark:text-gray-300 text-sm font-bold mb-2">
              Select Knowledge Base
            </label>
            <select
              value={baseId || ''}
              onChange={(e) => setBaseId(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              {bases.map(base => (
                <option key={base.id} value={base.id}>
                  {base.name}
                </option>
              ))}
            </select>
          </div>
        )}

        {/* Message */}
        <div className="mb-6 text-center text-gray-600 dark:text-gray-400">
          <p className="text-lg">{t('message.welcome')}</p>
          <p className="text-sm mt-1">{t('message.inspiration')}</p>
        </div>

        {/* Chat Input */}
        <form onSubmit={handleSubmit} className="bg-white dark:bg-slate-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-slate-700">
          <div className="mb-4">
            <input
              type="text"
              placeholder="Idea title..."
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4"
              required
            />
            <textarea
              placeholder={t('treasury.chatPlaceholder')}
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows={5}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
              required
            />
          </div>

          <div className="flex gap-2">
            <button
              type="submit"
              disabled={loading}
              className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg transition disabled:opacity-50"
            >
              <Plus size={20} />
              {loading ? t('common.loading') : t('common.create')}
            </button>
            <button
              type="button"
              className="flex items-center gap-2 bg-gray-200 dark:bg-slate-700 hover:bg-gray-300 dark:hover:bg-slate-600 text-gray-700 dark:text-gray-300 font-bold py-2 px-4 rounded-lg transition"
            >
              {t('treasury.voiceInput')}
            </button>
          </div>
        </form>

        {/* Features Info */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-blue-50 dark:bg-blue-900/30 rounded-lg p-4 border border-blue-200 dark:border-blue-800">
            <p className="text-blue-700 dark:text-blue-300 font-semibold text-sm">
              # {t('treasury.keepInput')}
            </p>
            <p className="text-blue-600 dark:text-blue-400 text-xs mt-1">Save input for later</p>
          </div>
          <div className="bg-green-50 dark:bg-green-900/30 rounded-lg p-4 border border-green-200 dark:border-green-800">
            <p className="text-green-700 dark:text-green-300 font-semibold text-sm">
              # {t('treasury.inspiration')}
            </p>
            <p className="text-green-600 dark:text-green-400 text-xs mt-1">Get AI suggestions</p>
          </div>
          <div className="bg-purple-50 dark:bg-purple-900/30 rounded-lg p-4 border border-purple-200 dark:border-purple-800">
            <p className="text-purple-700 dark:text-purple-300 font-semibold text-sm">
              # {t('treasury.talkToSelf')}
            </p>
            <p className="text-purple-600 dark:text-purple-400 text-xs mt-1">Reflect and brainstorm</p>
          </div>
        </div>
      </div>
    </div>
  );
}
