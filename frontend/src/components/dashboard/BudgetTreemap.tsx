import { useState, useEffect } from 'react';
import { Treemap, ResponsiveContainer, Tooltip } from 'recharts';
import { getBudgetData } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';

interface TreemapData {
  name: string;
  size: number;
  variance: number;
  actual: number;
  budget: number;
  fill: string;
  [key: string]: any; // Allow additional properties for recharts
}

interface CustomTooltipProps {
  active?: boolean;
  payload?: any[];
}

const CustomTooltip = ({ active, payload }: CustomTooltipProps) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    const budget = data.budget || 0;
    const actual = data.actual || 0;
    const variance = data.variance || 0;
    const variancePercent = budget > 0 ? ((variance / budget) * 100).toFixed(1) : '0.0';
    const status = variance < 0 ? 'Over Budget' : variance > 0 ? 'Under Budget' : 'On Budget';

    return (
      <div className="bg-white p-4 rounded-lg shadow-lg border border-gray-200">
        <p className="font-semibold text-gray-900 mb-2">{data.name || 'Unknown'}</p>
        <div className="space-y-1 text-sm">
          <p className="text-gray-600">
            Budget: <span className="font-medium text-gray-900">${budget.toLocaleString()}</span>
          </p>
          <p className="text-gray-600">
            Actual: <span className="font-medium text-gray-900">${actual.toLocaleString()}</span>
          </p>
          <p className={`font-medium ${variance < 0 ? 'text-red-600' : 'text-green-600'}`}>
            {status}: ${Math.abs(variance).toLocaleString()} ({variancePercent}%)
          </p>
        </div>
      </div>
    );
  }
  return null;
};

const CustomContent = (props: any) => {
  const { x, y, width, height, name, size, variance } = props;

  // Only show label if box is large enough
  if (width < 80 || height < 50) return null;

  const displaySize = size || 0;
  const displayVariance = variance || 0;

  return (
    <g>
      <text
        x={x + width / 2}
        y={y + height / 2 - 10}
        textAnchor="middle"
        fill="#fff"
        fontSize={14}
        fontWeight="600"
      >
        {name || 'Unknown'}
      </text>
      <text
        x={x + width / 2}
        y={y + height / 2 + 10}
        textAnchor="middle"
        fill="#fff"
        fontSize={12}
      >
        ${displaySize.toLocaleString()}
      </text>
      <text
        x={x + width / 2}
        y={y + height / 2 + 28}
        textAnchor="middle"
        fill={displayVariance < 0 ? '#fca5a5' : '#86efac'}
        fontSize={11}
        fontWeight="500"
      >
        {displayVariance < 0 ? 'Over' : displayVariance > 0 ? 'Under' : 'On'} Budget
      </text>
    </g>
  );
};

export function BudgetTreemap() {
  const { token } = useAuth();
  const [data, setData] = useState<TreemapData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchBudgetData = async () => {
      if (!token) return;

      try {
        setLoading(true);
        const response = await getBudgetData(token);

        if (response.error) {
          setError(response.error);
          return;
        }

        if (response.data && response.data.items) {
          // Group by category and aggregate
          const categoryMap = new Map<string, { budget: number; actual: number; variance: number }>();

          response.data.items.forEach((item: any) => {
            const category = item.category || 'Other';
            const existing = categoryMap.get(category) || { budget: 0, actual: 0, variance: 0 };

            categoryMap.set(category, {
              budget: existing.budget + (item.budget || 0),
              actual: existing.actual + (item.actual_spent || 0),
              variance: existing.variance + (item.variance || 0),
            });
          });

          // Convert to treemap format
          const treemapData: TreemapData[] = Array.from(categoryMap.entries()).map(([name, values]) => {
            // Determine color based on variance
            let fill = '#9ca3af'; // gray for on budget
            if (values.variance < -1000) {
              fill = '#ef4444'; // red for over budget
            } else if (values.variance > 1000) {
              fill = '#22c55e'; // green for under budget
            }

            return {
              name,
              size: values.budget,
              variance: values.variance,
              actual: values.actual,
              budget: values.budget,
              fill,
            };
          });

          setData(treemapData);
        }
      } catch (err) {
        setError('Failed to load budget data');
      } finally {
        setLoading(false);
      }
    };

    fetchBudgetData();
  }, [token]);

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Budget Breakdown</h2>
        <div className="h-[500px] flex items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Budget Breakdown</h2>
        <div className="h-[500px] flex items-center justify-center">
          <p className="text-red-600">{error}</p>
        </div>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Budget Breakdown</h2>
        <div className="h-[500px] flex items-center justify-center">
          <p className="text-gray-600">No budget data available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-8">
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-gray-900">Budget Breakdown by Category</h2>
        <p className="text-sm text-gray-600 mt-1">
          Interactive visualization showing budget allocation and performance
        </p>
      </div>

      {/* Legend */}
      <div className="flex gap-6 mb-4 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-green-500 rounded"></div>
          <span className="text-gray-700">Under Budget</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-red-500 rounded"></div>
          <span className="text-gray-700">Over Budget</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-gray-400 rounded"></div>
          <span className="text-gray-700">On Budget</span>
        </div>
      </div>

      {/* Treemap */}
      <ResponsiveContainer width="100%" height={500}>
        <Treemap
          data={data}
          dataKey="size"
          stroke="#fff"
          content={<CustomContent />}
          animationDuration={800}
        >
          <Tooltip content={<CustomTooltip />} />
        </Treemap>
      </ResponsiveContainer>

      {/* Summary Stats */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <p className="text-sm text-gray-600">Total Budget</p>
            <p className="text-lg font-semibold text-gray-900">
              ${data.reduce((sum, item) => sum + (item.budget || 0), 0).toLocaleString()}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Total Actual</p>
            <p className="text-lg font-semibold text-gray-900">
              ${data.reduce((sum, item) => sum + (item.actual || 0), 0).toLocaleString()}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Total Variance</p>
            <p className={`text-lg font-semibold ${data.reduce((sum, item) => sum + (item.variance || 0), 0) < 0 ? 'text-red-600' : 'text-green-600'}`}>
              ${Math.abs(data.reduce((sum, item) => sum + (item.variance || 0), 0)).toLocaleString()}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
