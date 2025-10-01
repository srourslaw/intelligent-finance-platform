import { LucideIcon } from 'lucide-react';

interface KPICardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  trend?: 'positive' | 'negative' | 'neutral';
  percentage?: number;
  showProgressBar?: boolean;
}

export function KPICard({
  title,
  value,
  subtitle,
  icon: Icon,
  trend = 'neutral',
  percentage,
  showProgressBar = false,
}: KPICardProps) {
  const trendColors = {
    positive: 'text-green-600 bg-green-50',
    negative: 'text-red-600 bg-red-50',
    neutral: 'text-blue-600 bg-blue-50',
  };

  const progressBarColor = {
    positive: 'bg-green-500',
    negative: 'bg-red-500',
    neutral: 'bg-blue-500',
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
        <div className={`p-3 rounded-lg ${trendColors[trend]}`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>

      {/* Subtitle or Progress Bar */}
      {showProgressBar && percentage !== undefined ? (
        <div className="mt-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs font-medium text-gray-600">Progress</span>
            <span className="text-xs font-semibold text-gray-900">{percentage}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all ${progressBarColor[trend]}`}
              style={{ width: `${Math.min(percentage, 100)}%` }}
            />
          </div>
        </div>
      ) : subtitle ? (
        <p className={`text-sm font-medium mt-2 ${
          trend === 'negative' ? 'text-red-600' :
          trend === 'positive' ? 'text-green-600' :
          'text-gray-600'
        }`}>
          {subtitle}
        </p>
      ) : null}
    </div>
  );
}
