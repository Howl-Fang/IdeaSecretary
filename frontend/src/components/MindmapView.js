import React, { useEffect, useRef, useState, useMemo } from 'react';
import { ZoomIn, ZoomOut } from 'lucide-react';

const MindmapView = ({ ideas, onEdit, onDelete, onAddChild, baseName }) => {
  const svgRef = useRef(null);
  const containerRef = useRef(null);
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 50, y: 50 });
  const [hoveredNode, setHoveredNode] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const dragStart = useRef({ x: 0, y: 0 });

  // Calculate node positions using hierarchical tree layout
  const calculateLayout = useMemo(() => {
    return (ideas) => {
      const positions = new Map();
      const nodeHeight = 80;
      const nodeWidth = 140;
      const horizontalSpacing = 200;
      const verticalSpacing = 120;

      let maxDepth = 0;
      const calculateDepth = (idea, depth = 0) => {
        maxDepth = Math.max(maxDepth, depth);
        if (idea.children) {
          idea.children.forEach(child => calculateDepth(child, depth + 1));
        }
      };
      ideas.forEach(idea => calculateDepth(idea));

      let y = 50;
      const processLevel = (ideaList, depth = 0, parentX = null) => {
        if (ideaList.length === 0) return;

        const totalWidth = ideaList.length * horizontalSpacing;
        const startX = Math.max(50, parentX ? parentX - totalWidth / 2 : 50);

        ideaList.forEach((idea, index) => {
          const x = startX + index * horizontalSpacing;
          positions.set(idea.id, { x, y });

          if (idea.children && idea.children.length > 0) {
            const childCenterX = x + nodeWidth / 2;
            processLevel(idea.children, depth + 1, childCenterX);
          }
        });

        y += verticalSpacing;
      };

      // Process all levels
      processLevel(ideas, 0);
      return positions;
    };
  }, []);

  const nodePositions = useMemo(() => {
    return calculateLayout(ideas);
  }, [ideas, calculateLayout]);

  // Generate SVG path from parent to child
  const generateConnector = (parentPos, childPos) => {
    const x1 = parentPos.x + 70;
    const y1 = parentPos.y + 40;
    const x2 = childPos.x + 70;
    const y2 = childPos.y;

    // Bezier curve path
    const controlY = (y1 + y2) / 2;
    return `M ${x1} ${y1} C ${x1} ${controlY}, ${x2} ${controlY}, ${x2} ${y2}`;
  };

  // Render all connectors recursively
  const renderConnectors = (ideaList) => {
    const connectors = [];

    const traverse = (idea) => {
      if (idea.children && idea.children.length > 0) {
        const parentPos = nodePositions.get(idea.id);
        idea.children.forEach(child => {
          const childPos = nodePositions.get(child.id);
          if (parentPos && childPos) {
            connectors.push(
              <path
                key={`line-${idea.id}-${child.id}`}
                d={generateConnector(parentPos, childPos)}
                stroke="#94a3b8"
                strokeWidth={2}
                fill="none"
                strokeLinecap="round"
                className="dark:stroke-slate-500"
              />
            );
          }
          traverse(child);
        });
      }
    };

    ideaList.forEach(idea => traverse(idea));
    return connectors;
  };

  // Render all nodes recursively
  const renderAllNodes = (ideaList) => {
    const nodes = [];

    const traverse = (idea) => {
      const pos = nodePositions.get(idea.id);
      if (!pos) return;

      const isHovered = hoveredNode === idea.id;
      const wordCount = idea.content ? idea.content.split(/\s+/).length : 0;
      const hasChildren = idea.children && idea.children.length > 0;

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
            width={140}
            height={40}
            rx={6}
            fill={isHovered ? '#818cf8' : '#ffffff'}
            stroke={isHovered ? '#6366f1' : '#cbd5e1'}
            strokeWidth={2}
            className="dark:fill-slate-700 dark:stroke-slate-600 transition-all"
          />

          {/* Node text */}
          <text
            x={pos.x + 70}
            y={pos.y + 15}
            textAnchor="middle"
            fontSize={11}
            fontWeight={600}
            fill={isHovered ? '#ffffff' : '#1f2937'}
            className="dark:fill-white pointer-events-none"
          >
            {idea.title.length > 14 ? idea.title.substring(0, 14) + '...' : idea.title}
          </text>

          <text
            x={pos.x + 70}
            y={pos.y + 28}
            textAnchor="middle"
            fontSize={9}
            fill={isHovered ? '#e5e7eb' : '#6b7280'}
            className="dark:fill-gray-400 pointer-events-none"
          >
            {wordCount} words {hasChildren ? `• ${idea.children.length}` : ''}
          </text>

          {/* Hover tooltip */}
          {isHovered && (
            <g>
              <rect
                x={pos.x + 150}
                y={pos.y - 20}
                width={220}
                height={90}
                rx={8}
                fill="#1f2937"
                opacity={0.95}
                className="dark:fill-slate-900"
              />
              <text
                x={pos.x + 160}
                y={pos.y - 5}
                fontSize={12}
                fontWeight={600}
                fill="#ffffff"
                className="pointer-events-none"
              >
                {idea.title}
              </text>
              <text
                x={pos.x + 160}
                y={pos.y + 15}
                fontSize={10}
                fill="#d1d5db"
                className="pointer-events-none"
              >
                {idea.content ? idea.content.substring(0, 40) + '...' : 'No content'}
              </text>
              <text
                x={pos.x + 160}
                y={pos.y + 35}
                fontSize={9}
                fill="#9ca3af"
                className="pointer-events-none"
              >
                {wordCount} words {idea.tags && idea.tags.length > 0 ? `• ${idea.tags.join(', ')}` : ''}
              </text>
            </g>
          )}
        </g>
      );

      // Traverse children
      if (idea.children && idea.children.length > 0) {
        idea.children.forEach(child => traverse(child));
      }
    };

    ideaList.forEach(idea => traverse(idea));
    return nodes;
  };

  // Handle zoom
  const handleZoom = (direction) => {
    setZoom(prev => {
      const newZoom = direction === 'in' ? prev + 0.1 : prev - 0.1;
      return Math.max(0.5, Math.min(3, newZoom));
    });
  };

  // Handle pan with mouse
  const handleMouseDown = (e) => {
    if (e.button === 2 || e.ctrlKey) { // Right click or Ctrl+click
      setIsDragging(true);
      dragStart.current = { x: e.clientX, y: e.clientY };
    }
  };

  const handleMouseMove = (e) => {
    if (isDragging) {
      const dx = e.clientX - dragStart.current.x;
      const dy = e.clientY - dragStart.current.y;
      setPan(prev => ({
        x: prev.x + dx,
        y: prev.y + dy
      }));
      dragStart.current = { x: e.clientX, y: e.clientY };
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  // Calculate SVG dimensions
  const svgWidth = 1400;
  const svgHeight = 900;
  return (
    <div className="w-full">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">{baseName}</h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            {ideas.length} root ideas • Right-click drag to pan • Use zoom buttons
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
          className="border border-gray-200 dark:border-slate-700 rounded-lg bg-gradient-to-b from-gray-50 to-white dark:from-slate-800 dark:to-slate-900 overflow-hidden"
          style={{ height: '600px', cursor: isDragging ? 'grabbing' : 'grab' }}
          onMouseDown={handleMouseDown}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseUp}
          onContextMenu={(e) => e.preventDefault()}
        >
          <svg
            ref={svgRef}
            width={svgWidth}
            height={svgHeight}
            style={{
              transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`,
              transformOrigin: '0 0',
              userSelect: 'none',
            }}
            className="select-none"
          >
            <defs>
              <marker
                id="arrowhead"
                markerWidth="10"
                markerHeight="7"
                refX="9"
                refY="3.5"
                orient="auto"
              >
                <polygon points="0 0, 10 3.5, 0 7" fill="#94a3b8" />
              </marker>
            </defs>

            {/* Connectors (drawn first, behind nodes) */}
            {renderConnectors(ideas)}

            {/* Nodes (drawn on top) */}
            {renderAllNodes(ideas)}
          </svg>
        </div>
      )}

      <div className="mt-4 p-4 bg-blue-50 dark:bg-slate-800 border border-blue-200 dark:border-slate-700 rounded-lg text-sm text-gray-700 dark:text-gray-300">
        <p>💡 <strong>Tips:</strong> Right-click and drag to pan, use zoom buttons to adjust view. Hover over nodes to see full details.</p>
      </div>
    </div>
  );
};

export default MindmapView;
