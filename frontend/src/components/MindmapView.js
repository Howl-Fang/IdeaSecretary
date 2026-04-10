import React, { useEffect, useRef, useState } from 'react';
import { ZoomIn, ZoomOut, Plus, Edit2, Trash2 } from 'lucide-react';

const MindmapView = ({ ideas, onEdit, onDelete, onAddChild, baseName }) => {
  const svgRef = useRef(null);
  const containerRef = useRef(null);
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [hoveredNode, setHoveredNode] = useState(null);
  const nodePositions = useRef(new Map());

  // Calculate node positions using force-directed layout
  const calculateLayout = (ideas) => {
    const positions = new Map();
    let y = 0;

    const traverse = (ideaList, x = 0, spacing = 250) => {
      ideaList.forEach((idea, index) => {
        const nodeX = x + index * spacing;
        const nodeY = y;
        positions.set(idea.id, { x: nodeX, y: nodeY });

        if (idea.children && idea.children.length > 0) {
          y += 150;
          traverse(idea.children, nodeX - (idea.children.length * spacing) / 2, spacing * 0.7);
          y += 150;
        }
      });
    };

    traverse(ideas, 100);
    return positions;
  };

  // Generate SVG path from parent to child
  const generatePath = (parentPos, childPos) => {
    const controlX = (parentPos.x + childPos.x) / 2;
    return `M ${parentPos.x + 60} ${parentPos.y + 30} Q ${controlX} ${(parentPos.y + childPos.y) / 2} ${childPos.x} ${childPos.y}`;
  };

  // Render nodes and connections
  const renderNodes = (ideaList, parentPos = null) => {
    const nodes = [];
    const connections = [];

    const traverse = (ideas) => {
      ideas.forEach((idea) => {
        const pos = nodePositions.current.get(idea.id);
        if (!pos) return;

        // Draw connection from parent to child
        if (parentPos) {
          connections.push(
            <path
              key={`conn-${idea.id}`}
              d={generatePath(parentPos, pos)}
              stroke="#cbd5e1"
              strokeWidth={2}
              fill="none"
              className="dark:stroke-slate-600"
            />
          );
        }

        // Draw node
        const isHovered = hoveredNode === idea.id;
        const wordCount = idea.content ? idea.content.split(/\s+/).length : 0;

        nodes.push(
          <g
            key={idea.id}
            className="cursor-pointer"
            onMouseEnter={() => setHoveredNode(idea.id)}
            onMouseLeave={() => setHoveredNode(null)}
          >
            {/* Node background */}
            <rect
              x={pos.x}
              y={pos.y}
              width={120}
              height={60}
              rx={8}
              fill={isHovered ? '#818cf8' : '#ffffff'}
              stroke={isHovered ? '#6366f1' : '#e2e8f0'}
              strokeWidth={2}
              className="dark:fill-slate-700 dark:stroke-slate-600"
            />

            {/* Node text */}
            <text
              x={pos.x + 60}
              y={pos.y + 20}
              textAnchor="middle"
              fontSize={12}
              fontWeight={600}
              fill={isHovered ? '#ffffff' : '#1f2937'}
              className="dark:fill-white pointer-events-none"
            >
              {idea.title.length > 12 ? idea.title.substring(0, 12) + '...' : idea.title}
            </text>

            <text
              x={pos.x + 60}
              y={pos.y + 40}
              textAnchor="middle"
              fontSize={10}
              fill={isHovered ? '#e5e7eb' : '#6b7280'}
              className="dark:fill-gray-400 pointer-events-none"
            >
              {wordCount} words
            </text>

            {/* Tooltip */}
            {isHovered && (
              <g>
                <rect
                  x={pos.x + 130}
                  y={pos.y - 10}
                  width={200}
                  height={80}
                  rx={6}
                  fill="#1f2937"
                  className="dark:fill-slate-900"
                  opacity={0.95}
                />
                <text
                  x={pos.x + 140}
                  y={pos.y + 10}
                  fontSize={12}
                  fontWeight={600}
                  fill="#ffffff"
                  className="pointer-events-none"
                >
                  {idea.title}
                </text>
                <text
                  x={pos.x + 140}
                  y={pos.y + 30}
                  fontSize={10}
                  fill="#d1d5db"
                  className="pointer-events-none"
                >
                  {idea.content ? idea.content.substring(0, 30) + '...' : 'No content'}
                </text>
              </g>
            )}
          </g>
        );

        // Traverse children
        if (idea.children && idea.children.length > 0) {
          const childResults = traverse(idea.children);
          nodes.push(...childResults.nodes);
          connections.push(...childResults.connections);
        }

        return { nodes, connections };
      });

      return { nodes, connections };
    };

    const result = traverse(ideas);
    return [result.connections, result.nodes];
  };

  // Calculate layout on mount and when ideas change
  useEffect(() => {
    if (ideas.length > 0) {
      nodePositions.current = calculateLayout(ideas);
    }
  }, [ideas]);

  // Handle zoom
  const handleZoom = (direction) => {
    setZoom(prev => {
      const newZoom = direction === 'in' ? prev + 0.1 : prev - 0.1;
      return Math.max(0.5, Math.min(3, newZoom));
    });
  };

  // Handle pan
  const handlePan = (e) => {
    if (e.buttons !== 2 && !e.ctrlKey) return; // Right click or Ctrl+drag
    setPan(prev => ({
      x: prev.x + e.movementX,
      y: prev.y + e.movementY
    }));
  };

  const [connections, nodeGraphics] = renderNodes(ideas);
  const width = Math.max(1200, Math.max(...Array.from(nodePositions.current.values()).map(p => p.x)) + 200);
  const height = Math.max(800, Math.max(...Array.from(nodePositions.current.values()).map(p => p.y)) + 150);

  return (
    <div className="w-full">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">{baseName}</h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            {ideas.length} root ideas • Drag to pan • Scroll wheel to zoom
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => handleZoom('in')}
            className="p-2 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg transition"
            title="Zoom in"
          >
            <ZoomIn size={20} className="text-gray-600 dark:text-gray-400" />
          </button>
          <button
            onClick={() => handleZoom('out')}
            className="p-2 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg transition"
            title="Zoom out"
          >
            <ZoomOut size={20} className="text-gray-600 dark:text-gray-400" />
          </button>
        </div>
      </div>

      {ideas.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 dark:bg-slate-800 rounded-lg">
          <p className="text-gray-600 dark:text-gray-400">No ideas to visualize</p>
        </div>
      ) : (
        <div
          ref={containerRef}
          className="border border-gray-200 dark:border-slate-700 rounded-lg bg-gray-50 dark:bg-slate-800 overflow-auto"
          style={{ height: '600px' }}
          onMouseMove={handlePan}
          onContextMenu={e => e.preventDefault()}
        >
          <svg
            ref={svgRef}
            width={width}
            height={height}
            style={{
              transform: `scale(${zoom}) translate(${pan.x}px, ${pan.y}px)`,
              transformOrigin: '0 0',
              cursor: 'grab',
            }}
          >
            {/* Connections (drawn first, behind nodes) */}
            {connections}
            {/* Nodes (drawn on top) */}
            {nodeGraphics}
          </svg>
        </div>
      )}

      <div className="mt-4 p-4 bg-blue-50 dark:bg-slate-800 border border-blue-200 dark:border-slate-700 rounded-lg text-sm text-gray-700 dark:text-gray-300">
        <p>💡 <strong>How to use:</strong> Right-click and drag to pan the mindmap, use zoom buttons to adjust view.</p>
      </div>
    </div>
  );
};

export default MindmapView;
