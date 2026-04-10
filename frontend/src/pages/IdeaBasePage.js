import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { ideasAPI } from '../services/api';
import { Plus } from 'lucide-react';

export default function IdeaBasePage() {
  const { t } = useTranslation();
  const [bases, setBases] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadBases();
  }, []);

  const loadBases = async () => {
    try {
      setLoading(true);
      const response = await ideasAPI.getBases();
      setBases(response.data.bases);
    } catch (error) {
      console.error('Failed to load bases:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex-1 p-6 flex items-center justify-center">
        <p>{t('common.loading')}</p>
      </div>
    );
  }

  return (
    <div className="flex-1 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            {t('nav.myIdeaBase')}
          </h1>
          <button className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg transition">
            <Plus size={20} />
            New Base
          </button>
        </div>

        {bases.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 dark:text-gray-400">
              {t('ideas.noIdeas')}
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {bases.map(base => (
              <div
                key={base.id}
                className="bg-white dark:bg-slate-800 rounded-lg shadow border border-gray-200 dark:border-slate-700"
              >
                <div className="p-6 border-b border-gray-200 dark:border-slate-700">
                  <div className="flex justify-between items-start mb-2">
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                      {base.name}
                    </h2>
                    <div className="text-sm text-gray-500 dark:text-gray-400">
                      {base.idea_count} ideas • {base.total_word_count} words
                    </div>
                  </div>
                  {base.description && (
                    <p className="text-gray-600 dark:text-gray-400">
                      {base.description}
                    </p>
                  )}
                </div>

                <div className="p-6">
                  {base.idea_count === 0 ? (
                    <p className="text-gray-500 dark:text-gray-400 text-center py-8">
                      No ideas yet
                    </p>
                  ) : (
                    <p className="text-gray-500 dark:text-gray-400">
                      {base.idea_count} ideas organized in this base
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
