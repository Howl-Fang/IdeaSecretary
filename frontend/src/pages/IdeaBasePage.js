import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { ideasAPI } from '../services/api';
import { Plus, ArrowLeft, GitBranch, Share2 } from 'lucide-react';
import TreeView from '../components/TreeView';
import MindmapView from '../components/MindmapView';

export default function IdeaBasePage() {
  const { t } = useTranslation();
  const [bases, setBases] = useState([]);
  const [selectedBase, setSelectedBase] = useState(null);
  const [treeData, setTreeData] = useState(null);
  const [viewMode, setViewMode] = useState('tree'); // 'tree' or 'mindmap'
  const [loading, setLoading] = useState(true);
  const [loadingTree, setLoadingTree] = useState(false);

  useEffect(() => {
    loadBases();
    // Load user's view preference from localStorage
    const savedViewMode = localStorage.getItem('ideaViewMode');
    if (savedViewMode) setViewMode(savedViewMode);
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

  const loadBaseTree = async (baseId) => {
    try {
      setLoadingTree(true);
      const response = await ideasAPI.getTree(baseId);
      setTreeData(response.data.ideas || []);
      setSelectedBase(bases.find(b => b.id === baseId));
    } catch (error) {
      console.error('Failed to load idea tree:', error);
      setTreeData([]);
    } finally {
      setLoadingTree(false);
    }
  };

  const handleViewModeChange = (mode) => {
    setViewMode(mode);
    localStorage.setItem('ideaViewMode', mode);
  };

  const handleEdit = (idea) => {
    console.log('Edit idea:', idea);
    // TODO: Implement edit dialog
  };

  const handleDelete = async (ideaId) => {
    if (!window.confirm('Are you sure you want to delete this idea?')) return;
    try {
      await ideasAPI.deleteIdea(ideaId);
      // Reload tree
      if (selectedBase) {
        await loadBaseTree(selectedBase.id);
      }
    } catch (error) {
      console.error('Failed to delete idea:', error);
    }
  };

  const handleAddChild = (parentId) => {
    console.log('Add child to:', parentId);
    // TODO: Implement add child dialog
  };

  if (loading) {
    return (
      <div className="flex-1 p-6 flex items-center justify-center">
        <p>{t('common.loading')}</p>
      </div>
    );
  }

  // Show tree view for selected base
  if (selectedBase) {
    return (
      <div className="flex-1 p-6 overflow-auto">
        <div className="max-w-7xl mx-auto">
          {/* Header with back button */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4">
              <button
                onClick={() => {
                  setSelectedBase(null);
                  setTreeData(null);
                }}
                className="p-2 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg transition"
                title="Back to bases"
              >
                <ArrowLeft size={24} className="text-gray-600 dark:text-gray-400" />
              </button>
              <div>
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                  {selectedBase.name}
                </h1>
                {selectedBase.description && (
                  <p className="text-gray-600 dark:text-gray-400 mt-1">
                    {selectedBase.description}
                  </p>
                )}
              </div>
            </div>
            <button className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg transition">
              <Plus size={20} />
              New Idea
            </button>
          </div>

          {/* View mode toggle */}
          <div className="flex gap-2 mb-6 bg-white dark:bg-slate-800 w-fit p-1 rounded-lg border border-gray-200 dark:border-slate-700">
            <button
              onClick={() => handleViewModeChange('tree')}
              className={`flex items-center gap-2 px-4 py-2 rounded-md transition ${
                viewMode === 'tree'
                  ? 'bg-indigo-600 text-white'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-700'
              }`}
            >
              <GitBranch size={18} />
              Tree View
            </button>
            <button
              onClick={() => handleViewModeChange('mindmap')}
              className={`flex items-center gap-2 px-4 py-2 rounded-md transition ${
                viewMode === 'mindmap'
                  ? 'bg-indigo-600 text-white'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-700'
              }`}
            >
              <Share2 size={18} />
              Mindmap
            </button>
          </div>

          {/* Content */}
          {loadingTree ? (
            <div className="text-center py-12">
              <p className="text-gray-600 dark:text-gray-400">{t('common.loading')}</p>
            </div>
          ) : viewMode === 'tree' ? (
            <TreeView
              ideas={treeData}
              baseName={selectedBase.name}
              onEdit={handleEdit}
              onDelete={handleDelete}
              onAddChild={handleAddChild}
            />
          ) : (
            <MindmapView
              ideas={treeData}
              baseName={selectedBase.name}
              onEdit={handleEdit}
              onDelete={handleDelete}
              onAddChild={handleAddChild}
            />
          )}
        </div>
      </div>
    );
  }

  // Show bases list
  return (
    <div className="flex-1 p-6 overflow-auto">
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
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {bases.map(base => (
              <div
                key={base.id}
                onClick={() => loadBaseTree(base.id)}
                className="bg-white dark:bg-slate-800 rounded-lg shadow border border-gray-200 dark:border-slate-700 hover:shadow-lg cursor-pointer transition"
              >
                <div className="p-6 border-b border-gray-200 dark:border-slate-700">
                  <div className="flex justify-between items-start mb-2">
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                      {base.name}
                    </h2>
                    <div className="text-sm text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-slate-700 px-3 py-1 rounded-full">
                      {base.idea_count}
                    </div>
                  </div>
                  {base.description && (
                    <p className="text-gray-600 dark:text-gray-400 text-sm">
                      {base.description}
                    </p>
                  )}
                </div>

                <div className="p-6 flex justify-between items-center">
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    {base.total_word_count} words total
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      loadBaseTree(base.id);
                    }}
                    className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm transition"
                  >
                    View Ideas
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
