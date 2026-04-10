import React, { useState } from 'react';
import { ChevronDown, ChevronRight, FileText, Trash2, Edit2, Plus } from 'lucide-react';

function TreeNode({ idea, onEdit, onDelete, onAddChild, depth = 0 }) {
  const [expanded, setExpanded] = useState(depth === 0);
  const hasChildren = idea.children && idea.children.length > 0;
  const wordCount = idea.content ? idea.content.split(/\s+/).length : 0;

  return (
    <div className="select-none">
      <div className="flex items-start gap-2 py-1 group">
        {/* Expand/Collapse Button */}
        <div className="w-6 flex-shrink-0 flex justify-center pt-1">
          {hasChildren ? (
            <button
              onClick={() => setExpanded(!expanded)}
              className="p-0 hover:bg-gray-200 dark:hover:bg-gray-600 rounded"
            >
              {expanded ? (
                <ChevronDown size={18} className="text-gray-600 dark:text-gray-400" />
              ) : (
                <ChevronRight size={18} className="text-gray-600 dark:text-gray-400" />
              )}
            </button>
          ) : (
            <div className="w-6" />
          )}
        </div>

        {/* Idea Content */}
        <div className="flex-1 min-w-0">
          <div className="bg-white dark:bg-slate-700 border border-gray-200 dark:border-slate-600 rounded-lg p-3 hover:shadow-md transition">
            <div className="flex items-start justify-between gap-3">
              <div className="flex-1 min-w-0">
                <h3 className="font-semibold text-gray-900 dark:text-white truncate">
                  {idea.title}
                </h3>
                {idea.content && (
                  <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2 mt-1">
                    {idea.content}
                  </p>
                )}
                <div className="flex items-center gap-2 mt-2 text-xs text-gray-500 dark:text-gray-400">
                  <FileText size={14} />
                  <span>{wordCount} words</span>
                  {idea.tags && idea.tags.length > 0 && (
                    <>
                      <span>•</span>
                      {idea.tags.map((tag, idx) => (
                        <span key={idx} className="px-2 py-0.5 bg-indigo-100 dark:bg-indigo-900 text-indigo-800 dark:text-indigo-200 rounded text-xs">
                          {tag}
                        </span>
                      ))}
                    </>
                  )}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition flex-shrink-0">
                <button
                  onClick={() => onAddChild(idea.id)}
                  className="p-1.5 hover:bg-blue-100 dark:hover:bg-blue-900 text-blue-600 dark:text-blue-400 rounded transition"
                  title="Add child idea"
                >
                  <Plus size={16} />
                </button>
                <button
                  onClick={() => onEdit(idea)}
                  className="p-1.5 hover:bg-yellow-100 dark:hover:bg-yellow-900 text-yellow-600 dark:text-yellow-400 rounded transition"
                  title="Edit idea"
                >
                  <Edit2 size={16} />
                </button>
                <button
                  onClick={() => onDelete(idea.id)}
                  className="p-1.5 hover:bg-red-100 dark:hover:bg-red-900 text-red-600 dark:text-red-400 rounded transition"
                  title="Delete idea"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          </div>

          {/* Children */}
          {expanded && hasChildren && (
            <div className="ml-2 mt-2 border-l-2 border-gray-300 dark:border-gray-600 pl-2">
              {idea.children.map(child => (
                <TreeNode
                  key={child.id}
                  idea={child}
                  onEdit={onEdit}
                  onDelete={onDelete}
                  onAddChild={onAddChild}
                  depth={depth + 1}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function TreeView({ ideas, onEdit, onDelete, onAddChild, baseName }) {
  return (
    <div className="w-full">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">{baseName}</h2>
        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
          {ideas.length} root ideas
        </p>
      </div>

      {ideas.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 dark:bg-slate-800 rounded-lg">
          <FileText size={48} className="mx-auto text-gray-400 dark:text-gray-500 mb-4" />
          <p className="text-gray-600 dark:text-gray-400">No ideas yet. Create your first idea!</p>
        </div>
      ) : (
        <div className="space-y-2">
          {ideas.map(idea => (
            <TreeNode
              key={idea.id}
              idea={idea}
              onEdit={onEdit}
              onDelete={onDelete}
              onAddChild={onAddChild}
            />
          ))}
        </div>
      )}
    </div>
  );
}
