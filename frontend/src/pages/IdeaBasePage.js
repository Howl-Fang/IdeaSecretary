import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { ideasAPI } from '../services/api';
import { ChevronDown, ChevronRight, Plus, Edit, Trash2 } from 'lucide-react';

export default function IdeaBasePage() {
  const { t } = useTranslation();
  const [bases, setBases] = useState([]);
  const [expandedIds, setExpandedIds] = useState(new Set());
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

  const toggleExpanded = (id) => {
    const newExpanded = new Set(expandedIds);
    if (newExpanded.has(id)) {
      newExpanded.delete(id);
    } else {
      newExpanded.add(id);
    }
    setExpandedIds(newExpanded);
  };

  const renderIdeaTree = (ideas, depth = 0) => {
    return ideas.map(idea => (
      <div key={idea.id} className={`ml-${depth * 4}`}>
        <div className="flex items-center gap-2 p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-slate-700 group">
          <button
            onClick={() => toggleExpanded(idea.id)}
            className="flex-shrink-0"
          >
            {idea.children && idea.children.length > 0 ? (
              expandedIds.has(idea.id) ? (
                <ChevronDown size={18} className="text-gray-400" />
              ) : (
                <ChevronRight size={18} className="text-gray-400" />
              )
            ) : (
              <div className="w-5" />
            )}
          </button>
          <div className="flex-1 min-w-0">
            <h4 className="font-semibold text-gray-900 dark:text-white truncate">
              {idea.title}
            </h4>
            <p className="text-sm text-gray-500 dark:text-gray-400 truncate line-clamp-1">
              {idea.content}
            </p>
          </div>
          <div className="flex-shrink-0 hidden group-hover:flex gap-1">
            <button className="p-1 hover:bg-gray-200 dark:hover:bg-slate-600 rounded">
              <Edit size={16} className="text-gray-600 dark:text-gray-300" />
            </button>
            <button className="p-1 hover:bg-red-100 dark:hover:bg-red-900 rounded">
              <Trash2 size={16} className="text-red-600 dark:text-red-400" />
            </button>
          </div>
        </div>

        {expandedIds.has(idea.id) && idea.children && idea.children.length > 0 && (
          <div className="ml-6">
            {renderIdeaTree(idea.children, depth + 1)}
          </div>
        )}
      </div>
    ));
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
                    <div className="space-y-2">
                      {/* Placeholder for tree rendering - implement after loading individual base */}
                      <p className="text-gray-500 dark:text-gray-400">
                        Ideas will load when implemented
                      </p>
                    </div>
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
